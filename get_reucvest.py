import requests

web = "https://gdz.ru/class-8/matematika"
main_url1 = f"{web}/bucko-proverochnye-raboty/"
result1 = requests.post(main_url1, data = {'name': "Musia"})
print(result1)