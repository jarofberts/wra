from datetime import date
from enum import Enum
from typing import List


def enum_options(enum):
    return [{'desc': member.replace('_', ' ').capitalize(), 'value': value.value} for member, value in enum.__members__.items()]


def get_enum_member_by_value(enum_type, value):
    for member_value in enum_type.__members__.values():
        if member_value.value == int(value):
            return member_value


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


class EducationLevel(Enum):
    LESS_THAN_12TH_GRADE = 1
    HIGH_SCHOOL = 2
    GED = 3
    SOME_COLLEGE = 4
    COLLEGE_AA = 5
    COLLEGE_BA = 6
    COLLEGE_BS = 7
    SOME_TRADE_SCHOOL = 8
    TRADE_SCHOOL_CERTIFICATE = 9


class Client(object):
    @staticmethod
    def keys():
        return [
            ['name_last', 'name_first', 'name_middle']
        ]

    @staticmethod
    def dynamodb_table_def():
        return {
            'KeySchema': [
                {'KeyType': 'HASH', 'AttributeName': 'id'},
                {'KeyType': 'RANGE', 'AttributeName': 'last+first+middle'}
            ],
            'AttributeDefinition': [
                {'AttributeName': 'id', 'AttributeType': 'N'},
                {'AttributeName': 'last+first+middle', 'AttributeType': 'S'}
            ],
            'LocalSecondaryIndexes': [
                {
                    'IndexName': 'name',
                    'KeySchema': [
                        {'KeyType': 'HASH', 'AttributeName': 'id'},
                        {'KeyType': 'RANGE', 'AttributeName': 'last+first+middle'}
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['last', 'first', 'middle']
                    }
                },
                {
                    'IndexName': 'pickled',
                    'KeySchema': [
                        {'KeyType': 'HASH', 'AttributeName': 'id'},
                        {'KeyType': 'RANGE', 'AttributeName': 'last+first+middle'}
                    ],
                    'Projection': {
                        'ProjectionType': 'INCLUDE',
                        'NonKeyAttributes': ['pickled']
                    }
                }
            ]
        }

    def __iter__(self):
        yield 'name', {'first': self.name_first, 'middle': self.name_middle, 'last': self.name_last}
        yield 'emergency_contact', {'name': self.emergency_contact_name, 'phone': self.emergency_contact_phone}
        yield 'gender', self.gender
        yield 'birth_date', self.birth_date
        yield 'address', {'street': self.address_street, 'city': self.address_city, 'state': self.address_state, 'zipcode': self.address_zipcode}
        yield 'phone', {'number': self.phone_number, 'type': self.phone_type, 'voicemail': self.phone_voicemail}
        yield 'email', self.email
        yield 'unemployed', {'status': self.unemployed_status, 'date': self.unemployed_date}
        yield 'employment_status', {
            'self_employed': self.employment_status_self_employed,
            'under_employed': self.employment_status_under_employed,
            'full_time': self.employment_status_full_time,
            'part_time': self.employment_status_part_time,
            'seasonal': self.employment_status_seasonal,
            'employer': self.employment_status_employer
        }
        yield 'lost_income', {
            'recent': self.lost_income_recent,
            'reason': {
                'lost_spouse_job': self.lost_income_reason_lost_job_spouse,
                'lost_self_job': self.lost_income_reason_lost_job_self,
                'lost_child_support': self.lost_income_reason_lost_child_support,
                'lost_gov_subsidy': self.lost_income_reason_lost_gov_subsidy,
                'other': self.lost_income_reason_other
            }
        }
        yield 'industries', self.industries
        yield 'citizenship', self.citizenship
        yield 'military', {
            'branch': {
                'air_force': self.military_branch_air_force,
                'army': self.military_branch_army,
                'coast_guard': self.military_branch_coast_guard,
                'marines': self.military_branch_marines,
                'national_guard': self.military_branch_national_guard,
                'navy': self.military_branch_navy,
            },
            'status': {
                'active': self.military_status_active,
                'injured': self.military_status_injured,
                'retired': self.military_status_retired,
                'reserves': self.military_status_reserves,
                'spouse': self.military_status_spouse
            }
        }
        yield 'domestic_violence_concerns', self.household_domestic_violence_concerns
        yield 'marital_status', self.household_marital_status
        yield 'single_parent', self.household_single_parent
        yield 'responsible_bills', self.household_responsible_bills
        yield 'household_annual_income', self.household_annual_income
        yield 'household_size', self.household_size
        yield 'household_minor_children', self.household_number_minor_children
        yield 'household_adult_children', self.household_number_adult_children
        yield 'homeless', {'currently': self.household_homeless_currently, 'chronic': self.household_homeless_chronic}
        yield 'household_head_female', self.household_head_female
        yield 'ethnicity', {
            'white': self.ethnicity_white,
            'black': self.ethnicity_black,
            'asian': self.ethnicity_asian,
            'native': self.ethnicity_native,
            'pacific': self.ethnicity_pacific,
            'other': self.ethnicity_other
        }
        yield 'language', {'english_2nd': self.language_english_2nd, 'known': self.language_known}
        yield 'education_level', {
            'lt_hs': self.education_level_lt_hs,
            'hs_diploma': self.education_level_hs_diploma,
            'ged': self.education_level_ged,
            'some_trade': self.education_level_some_trade,
            'trade_cert': self.education_level_trade_cert,
            'some_college': self.education_level_some_college,
            'college_aa': self.education_level_college_aa,
            'college_ba': self.education_level_college_ba,
            'college_bs': self.education_level_college_bs,
            'currently_attending': self.education_level_currently_attending
        }
        yield 'disabilities', {
            'abused_child': self.disabilities_child_abused,
            'neglected_child': self.disabilities_child_neglected,
            'severe_mental': self.disabilities_severe_mental,
            'developmental': self.disabilities_developmental,
            'elderly': self.disabilities_elderly,
            'frail': self.disabilities_frail,
            'physical': self.disabilities_physical,
            'hiv_aids': self.disabilities_hiv_aids,
            'drug_alcohol_abuse': self.disabilities_drug_alcohol_abuse
        }
        yield 'transportation', {'car': self.transportation_car, 'bus': self.transportation_bus, 'other': self.transportation_other}
        yield 'agency', {
            'name': self.agency_name,
            'counselor': {
                'name': self.agency_counselor,
                'phone': self.agency_counselor_phone,
                'email': self.agency_counselor_email
            }
        }
        yield 'photo_id', self.photo_id
        yield 'social_security_card', self.social_security_card
        yield 'previous_client', {'status': self.previous_client, 'date': self.previous_client_when}
        yield 'convicted', self.convicted
        yield 'can_background_check', self.can_background_check
        yield 'affirmed', {
            'signature': self.affirmed_signature,
            'name': self.affirmed_name,
            'date': self.affirmed_date
        }
        yield 'accept_not_counseling', {
            'signature': self.accept_not_counseling_signature,
            'name': self.accept_not_counseling_name,
            'date': self.accept_not_counseling_date
        }

    @staticmethod
    def field_groups():
        groups = [
                {
                    'name': 'Contact Information',
                    'sub_groups': [
                        {
                            'sub_group': 'Name',
                            'members': [
                                {'field': 'name_first', 'type': 'str', 'desc': 'first', 'required': True},
                                {'field': 'name_middle', 'type': 'str', 'desc': 'middle'},
                                {'field': 'name_last', 'type': 'str', 'desc': 'last', 'required': True}]
                        }, {
                            'members': [
                                {'field': 'gender', 'type': 'Enum', 'desc': 'Gender', 'options': enum_options(Gender)},
                                {'field': 'birth_date', 'type': 'month', 'desc': 'Birth Date', 'required': True}]
                        }, {
                            'sub_group': 'Address',
                            'members': [
                                {'field': 'address_street', 'type': 'str', 'desc': 'Street'},
                                {'field': 'address_city', 'type': 'str', 'desc': 'City'},
                                {'field': 'address_state', 'type': 'str', 'desc': 'State'},
                                {'field': 'address_zipcode', 'type': 'str', 'desc': 'Zip Code'}]
                        }, {
                            'sub_group': 'Phone',
                            'members': [
                                {'field': 'phone_number', 'type': 'str', 'desc': 'Number'},
                                {'field': 'phone_type', 'type': 'Enum', 'desc': 'Type', 'options': enum_options(PhoneType)},
                                {'field': 'phone_voicemail', 'type': 'bool', 'desc': 'Leave message'}]
                        }, {
                            'sub_group': 'Email',
                            'members': [
                                {'field': 'email', 'type': 'str,email', 'desc': 'Email address'}]
                        }, {
                            'sub_group': 'Emergency Contact',
                            'members': [
                                {'field': 'emergency_contact_name', 'type': 'str', 'desc': 'name'},
                                {'field': 'emergency_contact_phone', 'type': 'str', 'desc': 'phone'}]
                        }, {
                            'sub_group': 'Referring Agency',
                            'members': [
                                {'field': 'agency_name', 'type': 'str', 'desc': 'name'},
                                {'field': 'agency_counselor', 'type': 'str', 'desc': 'counselor'},
                                {'field': 'agency_counselor_phone', 'type': 'str', 'desc': 'phone'},
                                {'field': 'agency_counselor_email', 'type': 'str', 'desc': 'email'}
                            ]
                        }, {
                            'sub_group': 'Mode of transportation',
                            'members': [
                                {'field': 'transportation_car', 'type': 'bool', 'desc': 'Car'},
                                {'field': 'transportation_bus', 'type': 'bool', 'desc': 'Bus'},
                                {'field': 'transportation_other', 'type': 'str', 'desc': 'Other'}
                            ]
                        }
                    ]
                },
                {
                    'name': 'Employment',
                    'sub_groups': [
                        {
                            'sub_group': 'Unemployed',
                            'members': [
                                {'field': 'unemployed_status', 'type': 'bool', 'desc': 'Unemployed?'},
                                {'field': 'unemployed_date', 'type': 'month', 'desc': 'When unemployed?'}
                            ]
                        }, {
                            'sub_group': 'Employment',
                            'members': [
                                {'field': 'employment_status', 'type': 'int,Enum', 'desc': 'Status',
                                 'options': [{'desc': 'self-employed', 'value': 1},
                                             {'desc': 'under-employed', 'value': 2},
                                             {'desc': 'full-time', 'value': 4},
                                             {'desc': 'part-time', 'value': 8},
                                             {'desc': 'seasonal', 'value': 16}
                                             ]},
                                {'field': 'employment_status_employer', 'type': 'str', 'desc': 'Employer'}
                            ]
                        }, {
                            'sub_group': 'Lost Income',
                            'members': [
                                {'field': 'lost_income_recent', 'type': 'bool', 'desc': 'Recently lost income?'},
                                {'field': 'lost_income_reason', 'type': 'int,Enum', 'desc': 'Cause of income loss',
                                 'options': [{'desc': 'Lost my job', 'value': 1},
                                             {'desc': 'Spouse/Partner lost job', 'value': 2},
                                             {'desc': 'Loss/Lack of child support', 'value': 4},
                                             {'desc': 'Loss of government subsidy', 'value': 8}
                                             ]},
                                {'field': 'lost_income_reason_other', 'type': 'str', 'desc': 'Other'}
                            ]
                        }, {
                            'sub_group': "Industries I'm looking for",
                            'members': [
                                {'field': 'industries', 'type': 'str', 'count': 3}
                            ]
                        }
                    ]
                },
                {
                    'name': 'Demographics',
                    'sub_groups': [
                        {'sub_group': 'Cultural',
                         'members': [
                             {'field': 'ethnicity', 'type': 'int,Enum', 'desc': 'Ethnicity',
                              'options': [
                                  {'desc': 'White', 'value': 1},
                                  {'desc': 'Black/African American', 'value': 2},
                                  {'desc': 'Asian', 'value': 4},
                                  {'desc': 'American Indian/Alaskan Native', 'value': 8},
                                  {'desc': 'Native Hawaiian/Other Pacific Islander', 'value': 16}
                              ]},
                             {'field': 'ethnicity_other', 'type': 'str', 'desc': 'Other ethnicity'},
                         ]},
                        {'sub_group': 'Languages Spoken',
                         'members': [
                             {'field': 'language_english_2nd', 'type': 'bool', 'desc': 'English is a second language'},
                             {'field': 'language_known', 'type': 'str', 'desc': 'List other languages spoken ', 'count_min': 1}
                         ]},
                        {'sub_group': 'Household',
                         'members': [
                             {'field': 'household_marital_status', 'type': 'Enum', 'desc': 'Marital Status',
                              'options': enum_options(MaritalStatus)},
                             {'field': 'household_annual_income', 'type': 'int', 'desc': 'Annual household income'},
                             {'field': 'household_issues', 'type': 'int,Enum', 'desc': 'Details',
                              'options': [
                                  {'desc': 'are you responsible for the bills', 'value': 1},
                                  {'desc': 'female headed household', 'value': 2},
                                  {'desc': 'single parent', 'value': 4}
                              ]},
                             {'field': 'household_size', 'type': 'int', 'desc': 'Size of household'},
                             {'field': 'household_number_minor_children', 'type': 'int', 'desc': 'Number of minor children'},
                             {'field': 'household_number_adult_children', 'type': 'int', 'desc': 'Number of adult children'},
                         ]},
                        {'sub_group': 'Education',
                         'members': [
                             {'field': 'education_level', 'type': 'Enum', 'desc': 'Education Level',
                              'options': enum_options(EducationLevel)},
                             {'field': 'education_currently_attending', 'type': 'bool', 'desc': 'Currently attending school'}
                         ]},
                        {'members': [
                            {'field': 'disabilities', 'type': 'int,Enum', 'desc': 'Special Needs',
                             'options': [
                                 {'desc': 'Abused child', 'value': 1},
                                 {'desc': 'Neglected child', 'value': 2},
                                 {'desc': 'Severe Mental Illness', 'value': 4},
                                 {'desc': 'Developmental Disabilities', 'value': 8},
                                 {'desc': 'Physical Disabilities', 'value': 16},
                                 {'desc': 'Victim of Domestic Violence', 'value': 32},
                                 {'desc': 'Elderly', 'value': 64},
                                 {'desc': 'Frail elderly', 'value': 128},
                                 {'desc': 'Alcohol and drug abuse', 'value': 256},
                                 {'desc': 'Living with HIV/AIDS', 'value': 512},
                                 {'desc': 'chronically homeless', 'value': 1024},
                                 {'desc': 'currently homeless', 'value': 2048},
                             ]}
                        ]},
                        {
                            'sub_group': 'Citizenship',
                            'members': [
                                {'field': 'citizenship', 'type': 'Enum', 'desc': 'Citizenship Status',
                                 'options': enum_options(Citizenship)},
                                {'field': 'photo_id', 'type': 'bool', 'desc': 'Photo ID?'},
                                {'field': 'social_security_card', 'type': 'bool', 'desc': 'Social Security Card?'}
                            ]
                        }, {
                            'sub_group': 'Military',
                            'members': [
                                {'field': 'military_branch', 'type': 'int,Enum', 'desc': 'Branch',
                                 'options': [{'desc': 'Air Force', 'value': 1},
                                             {'desc': 'Army', 'value': 2},
                                             {'desc': 'Coast Guard', 'value': 4},
                                             {'desc': 'Marines', 'value': 8},
                                             {'desc': 'National Guard', 'value': 16},
                                             {'desc': 'Navy', 'value': 32}]
                                 },
                                {'field': 'military_status', 'type': 'int,Enum', 'desc': 'Status',
                                 'options': [{'desc': 'Active', 'value': 1},
                                             {'desc': 'Injured', 'value': 2},
                                             {'desc': 'Retired', 'value': 4},
                                             {'desc': 'Reserves', 'value': 8},
                                             {'desc': 'Spouse', 'value': 16}]
                                 },
                            ]
                        },
                        {
                            'sub_group': 'Previous Client',
                            'members': [
                                {'field': 'previous_client', 'type': 'bool', 'desc': 'Used our services in the past'},
                                {'field': 'previous_client_when', 'type': 'month', 'desc': 'When?'}
                            ]
                        },
                        {
                            'sub_group': 'Criminal record',
                            'members': [
                                {'field': 'convicted', 'type': 'bool', 'desc': 'Been convicted of a felony'},
                                {'field': 'can_background_check', 'type': 'bool', 'desc': 'Can pass background check'}
                            ]
                        }
                    ]
                },
                {
                    'name': 'Acceptance',
                    'sub_groups': [
                        {
                            'sub_group': 'I affirm that this information is correct to the best of my knowledge',
                            'members': [
                                {'field': 'affirmed_signature', 'type': 'bytes', 'desc': 'Signature'},
                                {'field': 'affirmed_name', 'type': 'str', 'desc': 'Print Name'},
                                {'field': 'affirmed_date', 'type': 'date', 'desc': 'Date'},
                            ]
                        },
                        {
                            'sub_group': 'Services provided by WRA are psycho-educational in nature and are '
                                         'resource-based. We do not provide or are responsible for therapeutic '
                                         'counseling. We offer a list of providers for these services upon request',
                            'members': [
                                {'field': 'accept_not_counseling_signature', 'type': 'bytes', 'desc': 'Signature'},
                                {'field': 'accept_not_counseling_name', 'type': 'str', 'desc': 'Print Name'},
                                {'field': 'accept_not_counseling_date', 'type': 'date', 'desc': 'Date'},
                            ]
                        }
                    ]
                },
            ]
        return groups

    name_first: str = None
    name_middle: str = None
    name_last: str = None

    emergency_contact_name: str = None
    emergency_contact_phone: str = None

    gender: Gender = None

    birth_date: str = None

    address_street: str = None
    address_city: str = None
    address_state: str = None
    address_zipcode: str = None

    phone_number: str = None
    phone_type: PhoneType = None
    phone_voicemail: bool = None

    email: str = None

    unemployed_status: bool = None
    unemployed_date: str = None

    employment_status: int = None
    employment_status_employer: str = None

    lost_income_recent: bool = None
    lost_income_reason: int = None
    lost_income_reason_other: str = None

    industries: List[str] = None

    citizenship: Citizenship = None

    military_branch: int = None
    military_status: int = None

    household_marital_status: MaritalStatus = None
    household_annual_income: int = None
    household_size: int = None
    household_number_minor_children: int = None
    household_number_adult_children: int = None
    household_issues: int = None

    ethnicity: int = None
    ethnicity_other: str = None

    language_english_2nd: bool = None
    language_known: List[str] = None

    education_level: int = None
    education_currently_attending: bool = None

    disabilities: int = None

    transportation_car: bool = None
    transportation_bus: bool = None
    transportation_other: str = None

    agency_name: str = None
    agency_counselor: str = None
    agency_counselor_phone: str = None
    agency_counselor_email: str = None

    photo_id: bool = None
    social_security_card: bool = None

    previous_client: bool = None
    previous_client_when: str = None

    convicted: bool = None
    can_background_check: bool = None

    affirmed_signature: bytes = None
    affirmed_name: str = None
    affirmed_date: date = None

    accept_not_counseling_signature: bytes = None
    accept_not_counseling_name: str = None
    accept_not_counseling_date: date = None
