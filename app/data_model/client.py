from datetime import date
from enum import Enum
from typing import List


def enum_options(enum):
    return [{'desc': member.replace('_', ' ').capitalize(), 'value': value.value} for member, value in enum.__members__.items()]


def get_enum_member_by_value(enum_type, value):
    for member_value in enum_type.__members__.values():
        if str(member_value.value) == str(value):
            return member_value


class Citizenship(Enum):
    US_CITIZEN = 'US Citizen'
    GREEN_CARD = 'Green Card'
    VISA = 'Visa'
    UNDOCUMENTED = 'Undocumented'


class Gender(Enum):
    FEMALE = 'Female'
    MALE = 'Male'
    TRANS = 'Trans'


class MaritalStatus(Enum):
    SINGLE = 'Single'
    MARRIED = 'Married'
    SEPARATED = 'Separated'
    DIVORCED = 'Divorced'
    WIDOWED = 'Widowed'


class PhoneType(Enum):
    PERSONAL = 'Personal'
    SHARED = 'Shared'
    HOME = 'Home'
    WORK = 'Work'
    MOBILE = 'Mobile'
    LAND_LINE = 'Land Line'


class EducationLevel(Enum):
    LESS_THAN_12TH_GRADE = 'Less than 12th grade'
    HIGH_SCHOOL = 'High School Diploma'
    GED = 'GED'
    SOME_COLLEGE = 'Some College'
    COLLEGE_AA = 'College AA'
    COLLEGE_BA = 'College BA'
    COLLEGE_BS = 'College BS'
    SOME_TRADE_SCHOOL = 'Some Trade School'
    TRADE_SCHOOL_CERTIFICATE = 'Trade School Certificate'


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
                                {'field': 'gender', 'type': 'Enum', 'desc': 'Gender', 'options': enum_options(Gender), 'multiple': True},
                                {'field': 'birth_date', 'type': 'month', 'desc': 'Birth Date', 'required': True}]
                        }, {
                            'sub_group': 'Address',
                            'alignment': 'Vertical',
                            'members': [
                                {'field': 'address_street', 'type': 'str', 'desc': 'Street'},
                                {'field': 'address_city', 'type': 'str', 'desc': 'City'},
                                {'field': 'address_state', 'type': 'str', 'desc': 'State'},
                                {'field': 'address_zipcode', 'type': 'str', 'desc': 'Zip Code'}]
                        }, {
                            'sub_group': 'Phone',
                            'members': [
                                {'field': 'phone_number', 'type': 'str', 'desc': 'Number'},
                                {'field': 'phone_type', 'type': 'Enum', 'desc': 'Type', 'options': enum_options(PhoneType), 'multiple': True},
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
                            'alignment': 'Vertical',
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
                                {'field': 'employment_status', 'type': 'Enum', 'desc': 'Status', 'multiple': True,
                                 'options': [{'desc': 'self-employed', 'value': 'self-employed'},
                                             {'desc': 'under-employed', 'value': 'under-employed'},
                                             {'desc': 'full-time', 'value': 'full-time'},
                                             {'desc': 'part-time', 'value': 'part-time'},
                                             {'desc': 'seasonal', 'value': 'seasonal'}
                                             ]},
                                {'field': 'employment_status_employer', 'type': 'str', 'desc': 'Employer'}
                            ]
                        }, {
                            'sub_group': 'Lost Income',
                            'members': [
                                {'field': 'lost_income_recent', 'type': 'bool', 'desc': 'Recently lost income?'},
                                {'field': 'lost_income_reason', 'type': 'Enum', 'desc': 'Cause of income loss', 'multiple': True,
                                 'options': [{'desc': 'Lost my job', 'value': 'Lost my job'},
                                             {'desc': 'Spouse/Partner lost job', 'value': 'Spouse/Partner lost job'},
                                             {'desc': 'Loss/Lack of child support', 'value': 'Loss/Lack of child support'},
                                             {'desc': 'Loss of government subsidy', 'value': 'Loss of government subsidy'}
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
                             {'field': 'ethnicity', 'type': 'Enum', 'desc': 'Ethnicity', 'multiple': True,
                              'options': [
                                  {'desc': 'White', 'value': 'White'},
                                  {'desc': 'Black/African American', 'value': 'Black/African American'},
                                  {'desc': 'Asian', 'value': 'Asian'},
                                  {'desc': 'American Indian/Alaskan Native', 'value': 'American Indian/Alaskan Native'},
                                  {'desc': 'Native Hawaiian/Other Pacific Islander', 'value': 'Native Hawaiian/Other Pacific Islander'}
                              ]},
                             {'field': 'ethnicity_other', 'type': 'str', 'desc': 'Other ethnicity'},
                         ]},
                        {'sub_group': 'Languages Spoken',
                         'members': [
                             {'field': 'language_english_2nd', 'type': 'bool', 'desc': 'English is a second language'},
                             {'field': 'language_known', 'type': 'str', 'desc': 'Other languages spoken ', 'count_min': 1, 'multiple': True}
                         ]},
                        {'sub_group': 'Household',
                         'alignment': 'vertical',
                         'members': [
                             {'field': 'household_marital_status', 'type': 'Enum', 'desc': 'Marital Status',
                              'options': enum_options(MaritalStatus)},
                             {'field': 'household_annual_income', 'type': 'int', 'desc': 'Annual household income'},
                             {'field': 'household_issues', 'type': 'Enum', 'desc': 'Details', 'multiple': True,
                              'options': [
                                  {'desc': 'Responsible for the bills', 'value': 'Responsible for the bills'},
                                  {'desc': 'Female headed household', 'value': 'Female headed household'},
                                  {'desc': 'Single parent', 'value': 'Single parent'}
                              ]},
                             {'field': 'household_size', 'type': 'int', 'desc': 'Size of household'},
                             {'field': 'household_number_minor_children', 'type': 'int', 'desc': 'Number of minor children'},
                             {'field': 'household_number_adult_children', 'type': 'int', 'desc': 'Number of adult children'},
                         ]},
                        {'sub_group': 'Education',
                         'members': [
                             {'field': 'education_level', 'type': 'Enum', 'desc': 'Highest Education Level',
                              'options': enum_options(EducationLevel), 'multiple': True},
                             {'field': 'education_currently_attending', 'type': 'bool', 'desc': 'Currently attending school'}
                         ]},
                        {'members': [
                            {'field': 'disabilities', 'type': 'Enum', 'desc': 'Special Needs', 'multiple': True,
                             'options': [
                                 {'desc': 'Abused child', 'value': 'Abused child'},
                                 {'desc': 'Alcohol and drug abuse', 'value': 'Alcohol and drug abuse'},
                                 {'desc': 'Chronically homeless', 'value': 'Chronically homeless'},
                                 {'desc': 'Currently homeless', 'value': 'Currently homeless'},
                                 {'desc': 'Developmental Disabilities', 'value': 'Developmental Disabilities'},
                                 {'desc': 'Elderly', 'value': 'Elderly'},
                                 {'desc': 'Frail elderly', 'value': 'Frail elderly'},
                                 {'desc': 'Living with HIV/AIDS', 'value': 'Living with HIV/AIDS'},
                                 {'desc': 'Neglected child', 'value': 'Neglected child'},
                                 {'desc': 'Physical Disabilities', 'value': 'Physical Disabilities'},
                                 {'desc': 'Severe Mental Illness', 'value': 'Severe Mental Illness'},
                                 {'desc': 'Victim of Domestic Violence', 'value': 'Victim of Domestic Violence'},
                             ]}
                        ]},
                        {
                            'sub_group': 'Citizenship',
                            'alignment': 'Vertical',
                            'members': [
                                {'field': 'citizenship', 'type': 'Enum', 'desc': 'Citizenship Status',
                                 'options': enum_options(Citizenship)},
                                {'field': 'photo_id', 'type': 'bool', 'desc': 'Photo ID?'},
                                {'field': 'social_security_card', 'type': 'bool', 'desc': 'Social Security Card?'}
                            ]
                        }, {
                            'sub_group': 'Military',
                            'alignment': 'Vertical',
                            'members': [
                                {'field': 'military_branch', 'type': 'Enum', 'desc': 'Branch',
                                 'options': [{'desc': 'Air Force', 'value': 'Air Force'},
                                             {'desc': 'Army', 'value': 'Army'},
                                             {'desc': 'Coast Guard', 'value': 'Coast Guard'},
                                             {'desc': 'Marines', 'value': 'Marines'},
                                             {'desc': 'National Guard', 'value': 'National Guard'},
                                             {'desc': 'Navy', 'value': 'Navy'}]
                                 },
                                {'field': 'military_status', 'type': 'Enum', 'desc': 'Status',
                                 'options': [{'desc': 'Active', 'value': 'Active'},
                                             {'desc': 'Injured', 'value': 'Injured'},
                                             {'desc': 'Retired', 'value': 'Retired'},
                                             {'desc': 'Reserves', 'value': 'Reserves'},
                                             {'desc': 'Spouse', 'value': 'Spouse'}]
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
                                {'field': 'can_background_check', 'type': 'bool', 'desc': 'I can pass background check'}
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
                                {'field': 'affirmed_date', 'type': 'date', 'desc': 'Today\'s Date'},
                            ]
                        },
                        {
                            'sub_group': 'Services provided by WRA are psycho-educational in nature and are '
                                         'resource-based. We do not provide or are responsible for therapeutic '
                                         'counseling. We offer a list of providers for these services upon request',
                            'members': [
                                {'field': 'accept_not_counseling_signature', 'type': 'bytes', 'desc': 'Signature'},
                                {'field': 'accept_not_counseling_name', 'type': 'str', 'desc': 'Print Name'},
                                {'field': 'accept_not_counseling_date', 'type': 'date', 'desc': 'Today\'s Date'},
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

    gender: str = None

    birth_date: str = None

    address_street: str = None
    address_city: str = None
    address_state: str = None
    address_zipcode: str = None

    phone_number: str = None
    phone_type: str = None
    phone_voicemail: str = None

    email: str = None

    unemployed_status: str = None
    unemployed_date: str = None

    employment_status: str = None
    employment_status_employer: str = None

    lost_income_recent: str = None
    lost_income_reason: str = None
    lost_income_reason_other: str = None

    industries: List[str] = None

    citizenship: Citizenship = None

    military_branch: str = None
    military_status: str = None

    household_marital_status: str = None
    household_annual_income: str = None
    household_size: str = None
    household_number_minor_children: str = None
    household_number_adult_children: str = None
    household_issues: str = None

    ethnicity: str = None
    ethnicity_other: str = None

    language_english_2nd: str = None
    language_known: str = None

    education_level: str = None
    education_currently_attending: str = None

    disabilities: str = None

    transportation_car: str = None
    transportation_bus: str = None
    transportation_other: str = None

    agency_name: str = None
    agency_counselor: str = None
    agency_counselor_phone: str = None
    agency_counselor_email: str = None

    photo_id: str = None
    social_security_card: str = None

    previous_client: str = None
    previous_client_when: str = None

    convicted: str = None
    can_background_check: str = None

    affirmed_signature: bytes = None
    affirmed_name: str = None
    affirmed_date: date = None

    accept_not_counseling_signature: bytes = None
    accept_not_counseling_name: str = None
    accept_not_counseling_date: date = None
