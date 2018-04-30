from datetime import date
from enum import Enum
from typing import List, AnyStr

from wra.app.dynamodb_controller.map_object_table import dynamo_db_object_table_schema
from wra.app.data_model import PrimaryKey, RangeKey, HashKey, DynamoDbBacked


class Citizenship(Enum):
    US_CITIZEN = 1
    GREEN_CARD = 2
    VISA = 3
    UNDOCUMENTED = 4


class Gender(Enum):
    FEMALE = 1
    MALE = 2
    TRANS = 4


class MaritalStatus(Enum):
    SINGLE = 1
    MARRIED = 2
    SEPARATED = 3
    DIVORCED = 4
    WIDOWED = 5


class PhoneType(Enum):
    PERSONAL = 1
    SHARED = 2
    HOME = 4
    WORK = 8
    MOBILE = 16
    LAND_LINE = 32


class Demographics(DynamoDbBacked):
    domestic_violence_concerns: bool = None
    marital_status: MaritalStatus = None
    single_parent: bool = None
    responsible_bills: bool = None
    annual_household_income: int = None
    household_count: int = None
    minor_children_count: int = None
    adult_children_count: int = None

    ethnicity_white: bool = None
    ethnicity_black: bool = None
    ethnicity_asian: bool = None
    ethnicity_native: bool = None
    ethnicity_pacific: bool = None
    ethnicity_other: str = None
    lang_eng_2nd: bool = None
    languages: List[str] = None
    citizenship: Citizenship = None

    military_branch: MilitaryBranch
    military_status: MilitaryStatus
    military_injured: bool

    education_less_than_hs: bool = None
    education_hs_diploma: bool = None
    education_ged: bool = None
    education_some_trade: bool = None
    education_trade_cert: bool = None
    education_some_college: bool = None
    education_college_aa: bool = None
    education_college_ba: bool = None
    education_college_bs: bool = None
    education_currently_attending: bool = None

    homeless_currently: bool = None
    homeless_chronic: bool = None

    # female_headed_household: bool = None
    # elderly: bool = None
    # frail: bool = None
    # hiv_or_aids: bool = None
    # abused_child: bool = None
    # neglected_child: bool = None
    # disab_severe_mental: bool = None
    # disab_developmental: bool = None
    # disab_physical: bool = None
    # drug_or_alcohol_abuse: bool = None


class Client(DynamoDbBacked):
    @staticmethod
    def table_def():
        return {
            'KeySchema': [
                {'KeyType': 'HASH', 'AttributeName': 'id'},
                {'KeyType': 'RANGE', 'AttributeName': 'sort_key'}
            ],
            'AttributeDefinition': [
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'sort_key', 'AttributeType': 'S'},
                {'AttributeName': 'name.first', 'AttributeType': 'S'},
                {'AttributeName': 'name.middle', 'AttributeType': 'S'},
                {'AttributeName': 'name.last', 'AttributeType': 'S'},
                {'AttributeName': 'pickled', 'AttributeType': 'B'},
            ],
            'LocalSecondaryIndexes': [
                {
                    'IndexName': 'name',
                    'KeySchema': [
                        {'AttributeName': 'name.last', 'KeyType': 'HASH'},
                        {'AttributeName': 'name.first', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['name.middle']
                    }
                },
                {
                    'IndexName': 'pickled',
                    'KeySchema': [
                        {'AttributeName': 'name.last', 'KeyType': 'HASH'},
                        {'AttributeName': 'name.first', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['pickled']
                    }
                }
            ]
        }
    def __init__(self):
        self._data = {
            'name': {'first': None, 'middle': None, 'last': None},
            'emergency_contact_name': None,
            'emergency_contact_phone': None,
            'gender': None,
            'birth_date': None,
            'address': {'street': None, 'city': None, 'state': None, 'zipcode': None},
            'phone': {'number': None, 'type': None, 'voicemail': None},
            'email': None,
            'unemployed': {
                'date': None,
                'status': None
            },
            'employment': {
                'status': {
                    'self_employed': None,
                    'under_employed': None,
                    'full_time': None,
                    'part_time': None,
                    'seasonal': None
                },
                'employer': None,
            },
            'lost_income': {
                'recent': None,
                'reason': {
                    'spouse_lost_job': None,
                    'self_lost_job': None,
                    'lost_child_support': None,
                    'lost_gov_subsidy': None,
                    'other': None
                }
            },
            'industries': [],
            'citizenship': None,
            'military_branch': {
                'air_force': None,
                'army': None,
                'coast_guard': None,
                'marines': None,
                'national_guard': None,
                'navy': None
            },
            'military_status': {
                'active': None,
                'retired': None,
                'reserves': None,
                'spouse': None,
                'injured': None
            },
            'demographics': {
                'household_info': {
                    'domestic_violence_concerns': None,
                    'marital_status': None,
                    'single_parent': None,
                    'responsible_bills': None,
                    'annual_household_income': None,
                    'household_count': None,
                    'minor_children_count': None,
                    'adult_children_count': None,
                    'homeless': {'currently': None, 'chronic': None},
                    'female_headed_household': None
                },
                'ethnicity': {
                    'white': None,
                    'black': None,
                    'asian': None,
                    'native': None,
                    'pacific': None,
                    'other': None
                },
                'language': {
                    'languages_known': [],
                    'english_2nd': None
                },
                'highest_level_education': {
                    'education_less_than_hs': None,
                    'education_hs_diploma': None,
                    'education_ged': None,
                    'education_some_trade': None,
                    'education_trade_cert': None,
                    'education_some_college': None,
                    'education_college_aa': None,
                    'education_college_ba': None,
                    'education_college_bs': None,
                    'education_currently_attending': None
                },
                'disabilities': {
                    'abused_child': None,
                    'neglected_child': None,
                    'severe_mental': None,
                    'developmental': None,
                    'elderly': None,
                    'frail': None,
                    'physical': None,
                    'hiv_or_aids': None,
                    'drug_or_alcohol_abuse': None
                }
            }
        }
