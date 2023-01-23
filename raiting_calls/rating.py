import csv
import datetime
import pprint

import sipuni_api
from hashlib import md5
from urllib.parse import urlencode


from . import services
from secrets import get_secrets_value, save_secrets_value
import bitrix as bx24

FILE_NAME = "secrets.json"
COLS_CSV = {
  "direction": 3,
  "from_phone": 4,
  "to_phone": 5,
  "rating": 10,
  "language": 12
}


class Rating:
    def __init__(self) -> None:
        self.user = get_secrets_value("sipuni_user")
        self.token = get_secrets_value("sipuni_token")
        self.client = sipuni_api.Sipuni(self.user, self.token)

    def init(self):
        date = datetime.date.today()
        # from_date = datetime.datetime.strptime(get_secrets_value("sipuni_date"), "%Y-%m-%d")
        from_date = date - datetime.timedelta(days=2)
        to_date = date - datetime.timedelta(days=1)
        rating = self.get_rating(from_date, to_date)
        print(rating)
        self.save_rating_to_bx24(rating)

    def save_rating_to_bx24(self, records):
        for record in records:
            if not record.get("rating") or not record.get("phone"):
                continue

            # Поиск контакта в битрикс по номеру телефона
            phones = services.get_list_variation_phone(record["phone"])
            cmd_contact = [f"crm.contact.list?filter[PHONE]={phone}&select[]=ID" for phone in phones]
            contacts_ = bx24.requests_bath(cmd_contact).get("result")
            contacts = [contact[0].get("ID") for contact in contacts_ if contact]
            if not contacts:
                continue

            deals_ = bx24.request_bx("crm.deal.list", {
                "filter": {"CONTACT_ID": contacts[0]},
                "order": {"ID": "DESC"},
                "select": ["ID", ]
            })
            if "result" not in deals_ or not deals_["result"]:
                continue

            deals = deals_["result"]
            if not deals:
                # поиск сделки связанной с контактом
                cmd = {}
                cmd["company"] = f"crm.contact.company.items.get?id={contacts[0]}"
                cmd["deal"] = f"crm.deal.list?filter[COMPANY_ID]=$result[company][0][COMPANY_ID]&order[ID]=DESC&select[]=ID"
                resp_deals = bx24.requests_bath(cmd).get("result")
                if not resp_deals["company"] or not resp_deals["deal"]:
                    continue
                deals = resp_deals["deal"]

            if isinstance(deals, list) and deals:
                deal_id = deals[0].get("ID")
                print(record)
                print(deal_id)
                res = bx24.request_bx("crm.deal.update", {
                    "id": deal_id,
                    "fields":
                        {
                            "UF_CRM_1670388910": record["rating"],
                            "UF_CRM_1670388944": services.get_language_id_by_name(record["language"])
                        },
                    "params": {"REGISTER_SONET_EVENT": "Y"}
                })

    def save_date(self, date):
        date_str = date.strftime("%Y-%m-%d", )
        save_secrets_value("sipuni_date", date_str)

    def get_rating(self, from_date, to_date):
        rating_csv = self.client.get_call_stats(from_date=from_date, to_date=to_date)
        data_list = []
        for row in rating_csv.split("\n")[1:]:
            lst = row.split(";")
            if len(lst) > 15:
                index = COLS_CSV["from_phone"] if lst[COLS_CSV["direction"]] == "Входящая" else COLS_CSV["to_phone"]
                data_list.append({
                    "phone": lst[index],
                    "rating": lst[COLS_CSV["rating"]],
                    "language": lst[COLS_CSV["language"]],
                })
        return data_list




