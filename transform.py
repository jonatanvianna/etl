import googlemaps
import json
import pdb;
import pandas as pd

coord = [
(-30.00221199,-51.22552735),
(-30.02764286,-51.25084839),
(-30.02655075,-51.20207391),
(-30.06307018,-51.21643935),
(-30.03528083,-51.24316122),
(-30.0731661,-51.23823893 ),
(-30.04335422,-51.25911173),
(-30.0539081,-51.23780894 ),
(-30.03085498,-51.1976115 ),
(-29.99303501,-51.21864678)]




maps = googlemaps.Client(key='***REMOVED***')

csv = pd.read_csv('normalizated_data/data.csv', usecols=[1, 3])

def get_country():
    pass
def get_city():
    pass
def get_state():
    pass
def get_neigbour():
    pass
def get_street_number():
    pass
def get_street_name():
    pass
def get_postal_code():
    pass
# class Address:
#     def __init__(self):
#         self.street_number = 234
#         self.street_name = 'oie'

# def __srt__(self):
#     return


def get_address(address_components):
    address = {}

    for component in address_components:
        component_types = component.get('types', '')

        if 'country' in component_types:
            address.update({'country': component.get('long_name')})

        if 'administrative_area_level_1' in component_types:
            address.update({'state': component.get('short_name')})

        if 'administrative_area_level_2' in component_types:
            address.update({'city': component.get('long_name')})

        if 'sublocality_level_1' in component_types:
            address.update({'neighborhood': component.get('long_name')})

        if 'street_number' in component_types:
            address.update({'street_number': component.get('long_name')})

        if 'route' in component_types:
            address.update({'street_name': component.get('long_name')})

        if 'postal_code' in component_types:
            address.update({'postal_code': component.get('long_name')})

    if address:
        return address


def is_address_valid(address):
    address_components = ['country', 'state', 'city', 'neighborhood', 'street_number', 'street_name', 'postal_code', 'latitute', 'longitute']
    address_keys = address.keys()


    for key in address_keys:

        if key not in address_components:
            return False
    return True
    # if not address.get('country'):
    #     return False
    # if not address.get('state'):
    #     return False
    # if not address.get('city'):
    #     return False
    # if not address.get('neighborhood'):
    #     return False
    # if not address.get('street_number'):
    #     return False
    # if not address.get('street_name'):
    #     return False
    # if not address.get('postal_code'):
    #     return False
    # address_components = ['country', 'state', 'city', 'neighborhood', 'street_number', 'street_name', 'postal_code']
    # return True


count = -1
for number, coordinate in csv.iterrows():
    # print(number, coordinate.values[0], coordinate.values[1])
    # for n, i in enumerate(coord):
    result = maps.reverse_geocode((coordinate.values[0], coordinate.values[1]), result_type='street_address', location_type='ROOFTOP')
    if result:

        for o in result:
            address_components = o.get("address_components", "")
            if address_components:
                complete_address = get_address(address_components)
                if complete_address:
                    complete_address.update({'latitute': coordinate.values[0], 'longitute': coordinate.values[1]})
                    if is_address_valid(complete_address):
                        count += 1
                        print("Integrate data:")
                        # print(json.dumps(complete_address, indent=4, ensure_ascii=False))
                    else:
                        print("NOT Integrate data:")
                        print(json.dumps(complete_address, indent=4, ensure_ascii=False))
    print(f"CSV [{number}] - Valid [{count}] HAS" if result else f"CSV [{number}] - Valid [{count}] EMPTY {result}")




            # if o.get('formatted_address'):
            #     count += 1
            #     print(f"{number}-{count} - {o.get('formatted_address')}")

            # if o.get("address_components"):
            # for i in o.get("address_components"):
            #     if 'street_number' in i.get("types", ""):
            #         count = count + 1
            #         ha = i.get("long_name")
                    # print(f'{ko}-{count}  -  {i.get("long_name")}')
                # else:
                #     print(json.dumps(o, indent=4))
    #     if ha:
    #         print(f'{ki.values[0]}, {ki.values[1]}-ko[{ko}]-count[{count}]  -  {ha}')
    #         pdb.set_trace()
    #     else:
    #         print(f'{ki.values[0]} - {ki.values[1]}-ko[{ko}]')
    # else:
    #     print(f"{ki.values[0]}, {ki.values[1]} - Empty result? {result}")

        #             # pdb.set_trace()
            # print(addr.get("short_name"))
            # print(json.dumps(o, indent=4))
            # if 'route' in addr.get("types"):
            #     # pdb.set_trace()
            #     print(addr.get("long_name"))
            # # for k, v in addr.items():

            #     print(k)







