import json
from watson_developer_cloud import NaturalLanguageClassifierV1

natural_language_classifier = NaturalLanguageClassifierV1(
  username="12d46e8b-113d-4d41-a701-74f6c37dd3d3",
  password="UeuQMFovIniO")


status = natural_language_classifier.classify('ebd2f7x230-nlc-70275', '3 cups uncooked instant rice 3 cups water 1 (10 ounce) can diced tomatoes with green chilies undrained 1 tablespoon chicken bouillon granules 3/4 cup sour cream 1 1/2 cups shredded Cheddar cheese divided')
print(json.dumps(status, indent=2))