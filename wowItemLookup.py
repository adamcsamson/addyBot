import json
import requests
from pprint import pprint
from blizzardapi import BlizzardApi

def parseKeyword(array):
    keywordModified = ""
    wordCount = 0
    for words in array[1:]:
        if (wordCount == 0):
            keywordModified += words
        else:
            keywordModified += ("%20" + words)
        wordCount += 1
    return keywordModified


def displayItemStats(itemToSearch, normalItemName):
    finalReply = ""

    # API ENDPOINT SETUP
    api_client = BlizzardApi('#APICLIENT', '#APITOKEN')
    itemID = 0
    urlFirstHalf = 'https://us.api.blizzard.com/data/wow/search/item?namespace=static-us&name.en_US='
    urlSecHalf = '&orderby=id&_page=1&access_token=US1RwwGPcZY8CKTNTSorlhMU4JuELuKARq'
    fullURL = urlFirstHalf + itemToSearch + urlSecHalf
    itemSearchRequest = requests.get(fullURL)
    blizzardJSONData = itemSearchRequest.json()
    normalItemName = normalItemName.lower()
    normalItemName = normalItemName.rstrip()
    for items in blizzardJSONData['results']:
        nextItem = str(items['data']['name']['en_US'].lower())
        print("Checking " + normalItemName + " to " + nextItem)
        if normalItemName in nextItem:
            print("GRABBED " + normalItemName + " to " + nextItem)
            itemID = items['data']['id']
            break
    if (itemID == 0):
        return "Item was not able to be found. Please try another search term."
    else:
        print("Pulling data for item " + normalItemName + " ID: ",itemID)
    getItem = api_client.wow.game_data.get_item('us', 'en_US', itemID, True)
    itemDetails = getItem['preview_item']

    # PARSING ITEM DETAILS
    weaponSpeed = 'Speed 0.0'
    itemReqs = 'Requires level 0'
    itemType = itemDetails['inventory_type']['name']
    itemName = itemDetails['name']
    itemQuality = itemDetails['quality']['name']
    itemEffect = "Item has no additional effects."
    if 'spells' in itemDetails:
        itemEffectJSON = itemDetails['spells'][0]['description']
        itemEffect = json.dumps(itemEffectJSON)
    if 'requirements' in itemDetails:
        if 'level' in itemDetails['requirements']:
            itemReqs = itemDetails['requirements']['level']['display_string']

    # ITEM NAME AND RARITY
    finalReply += (itemName + " (" + itemQuality + ") \n")

    # ITEM TYPE LINE PRINT
    if 'item_subclass' in itemDetails:
        subclass = itemDetails['item_subclass']['name']
        finalReply += (itemType + " | " + subclass + "\n")
    else:
        finalReply += (itemType + "\n")

    if 'weapon' in itemDetails:
        weaponDamage = itemDetails['weapon']['damage']['display_string']
        if 'attack_speed' in itemDetails['weapon']:
            weaponSpeed = itemDetails['weapon']['attack_speed']['display_string']
        finalReply += (weaponDamage + " (" + weaponSpeed + ")\n")
    if 'armor' in itemDetails:
        armorValue = itemDetails['armor']['display']['display_string']
        finalReply += (armorValue + "\n")

    # PRINT STATS
    if 'stats' in itemDetails:
        for stats in itemDetails['stats']:
            currentStat = stats['display']['display_string']
            finalReply += (currentStat + "\n")

    # PRINT ADV DETAILS
    pprint(itemDetails)
    finalReply += (itemEffect + "\n" + itemReqs + "\n")
    return finalReply


