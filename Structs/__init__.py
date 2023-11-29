from Structs.Blume_filter import Blume_filter

keyword = [
    'Health', 'Health Condition',
    'Public Health', 'Healthcare',
    'Binary Classification', 'PMU',
    'Indian', "stroke",
    "glucose", "hypertension"
]


blume_filter = Blume_filter(200, 100)
blume_filter.extend(keyword)

