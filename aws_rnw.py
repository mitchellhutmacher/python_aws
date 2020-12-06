import json

if __name__ == "__main__":
    dict = {}
    with open("eov-response-1595521534337.json") as f:
        dict = json.load(f)
    for i in dict["valueBlocks"]:
        print("id: {}\nlabel: {}\ndescription: {}\nvalueStatements: {}\n".format(i["id"],
        i["label"], i["description"], i["valueStatements"]))
