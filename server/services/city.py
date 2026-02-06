from server.models.entities import*
import traceback
from server.config.applogging import ResponseLoggerMiddleware


class CityService:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.city_modelObj = CityDoc
        self.state_modelObj = StateDoc
        self.country_modelObj = CountryDoc

    def save(self, city):
        print(city.get('country_name'))
        print(city.get('state_name'))
        doc = self.city_modelObj(country=city.get('country_name'),
                                 state=city.get('state_name'),
                                 city_name=city.get('city_name'),
                                 city_desc=city.get('city_desc'),
                                 address=city.get('address'))
        doc.save()

    def city_posting(self, dataset):
        self.logging.info('request started for Posting in ' + str(__file__))
        country = self.country_modelObj.objects(country_name=dataset['country_name']).first()
        state = self.state_modelObj.objects(state_name=dataset['state_name'], country=country).first()
        try:
            city = {'country_name': state.country,
                    'state_name': state,
                    'city_name': dataset['city_name'],
                    'city_desc': dataset['city_desc'],
                    'address': dataset['address']}
            self.save(city)
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def city_update(self, dataset):
        try:
            operation = dataset['txn']
            (country, state, city) = operation.split('#')
            country_obj = self.country_modelObj.objects(country_name=country).first()
            state_obj = self.state_modelObj.objects(state_name=state, country=country_obj).first()
            update_obj = self.city_modelObj.objects(city_name=city, state=state_obj, country=country_obj)
            update_obj.update(set__city_name=dataset['city_name'],
                              set__city_desc=dataset['city_desc'],
                              set__address=dataset['address'])
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def status_edit(self, dataset):
        try:

            (country, state, city) = (dataset['country_name'], dataset['state_name'], dataset['city_name'])
            country_obj = self.country_modelObj.objects(country_name=country).first()
            state_obj = self.state_modelObj.objects(state_name=state, country=country_obj).first()
            update_obj = self.city_modelObj.objects(city_name=city, state=state_obj, country=country_obj)
            update_obj = self.city_modelObj.objects(city_name=dataset["city_name"])
            if dataset["status"].lower() == 'true':
                update_obj.update(set__status=bool(True))
            elif dataset["status"].lower() == 'false':
                update_obj.update(set__status=bool(False))
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def city_getall(self):
        try:
            rec_object = CityDoc.objects()
            data_list = []
            for x in rec_object:
                data_list.append({'country_name': x.country.country_name,
                                  'state_name': x.state.state_name,
                                  'city_name': x.city_name,
                                  'city_desc': x.city_desc,
                                  'address': x.address})
        except:
            data_list = []
            self.logging.error(traceback.format_exc())
        return data_list

    def get_records(self):
        return self.city_modelObj.objects()

    def pull_reference_data(self, country, state, city):
        if country and state and city:
            countryObj = self.country_modelObj.objects(country_name=country).first()
            stateobj = self.state_modelObj.objects(country=countryObj, state_name=state).first()
            obj = self.city_modelObj.objects(country=countryObj, state=stateobj, city_name=city)
        else:
            obj = self.city_modelObj.objects()
        return obj