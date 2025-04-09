from power_of_10 import PowerOf10

def test_get_athlete_by_id():
    
    po10 = PowerOf10()
    athlete = po10.get_athlete_by_id(1114055)
    assert athlete.name == "Murray Graham"
    assert athlete.club == "North Ayrshire"
    assert athlete.gender == "Male"
    assert athlete.age_group == "U13"
    assert athlete.county == ""
    assert athlete.region == "Scotland"
    assert athlete.nation == "Scotland"

"""
# Murray Graham https://www.thepowerof10.info/athletes/profile.aspx?athleteid=1114055
{
    "name": "Murray Graham",
    "club": "North Ayrshire",
    "gender": "Male",
    "age_group": "U13",
    "county": "",
    "region": "Scotland",
    "nation": "Scotland"
}
"""

def test_mock():
    po10 = PowerOf10()
    _ = po10._get_page_html("https://www.thepowerof10.info/athletes/profile.aspx?athleteid=1114055")
    print(po10._page_html)