import json

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
tempTable = dynamodb.Table('fiori-cache-table')
userStatsTable = dynamodb.Table('fiori-user-stats')
cardStatsTable = dynamodb.Table('fiori-card-stats')

def lambda_handler(event, context):
    # use input id to get array from db
    boosterPackId = event["boosterPackId"]
    userPrimaryKey = event['userId']
    cardStatusList = event["cardStatusList"]

    response = pullFromCacheTable(boosterPackId)
    
    # assign statuses to things
    # combinedData contains:::: scryId, price, name, status
    combinedData = [response[i].update({'status': cardStatusList[i]}) for i in range(len(cardStatusList))]

    #     {
    #         cardId:
    #         amount:
    #         number:
    #     }

    # update card table
    for card in combinedData:
        if card['status'] == "RIPPED":
            updateCardStatsTable(card['scryfallId'], card['price'])

    # {
    #     userId: 1,
    #     amount: 0
    # }

    # update user table
    userUpdateAmount = sum([n['price'] for n in combinedData if n['status'] == "RIPPED"])
    updateUserStatsTable(userPrimaryKey, userUpdateAmount)


def pullFromCacheTable(boosterPackId):
    
    try:
        response = tempTable.get_item(Key={'primary_key': boosterPackId})["pack"]
        return {
            'statusCode': 200,
            'body': response
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Data No Longer in Cache - User Took Too Long',
                'error': str(e)
            })
        }
    #can eventually delete early

def updateUserStatsTable(primaryKey, cardUpdateAmount):
    try:
        response = userStatsTable.update_item(
            Key={'primary_key': primaryKey},
            UpdateExpression='SET Amount = Amount + :amount',
            ExpressionAttributeValues={':amount': cardUpdateAmount},
            ReturnValues="ALL_NEW"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'UserStatsTable updated successfully',
                'updatedAttributes': response['Attributes']
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating UserStatsTable',
                'error': str(e)
            })
        }


def updateCardStatsTable(primaryKey, cardUpdateAmount):
    try:
        response = cardStatsTable.update_item(
            Key={'primary_key': primaryKey},
            UpdateExpression='SET Amount = Amount + :amount, Number = Number + 1',
            ExpressionAttributeValues={':amount': cardUpdateAmount},
            ReturnValues="ALL_NEW"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'CardStatsTable updated successfully',
                'updatedAttributes': response['Attributes']
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error updating CardStatsTable',
                'error': str(e)
            })
        }
    


