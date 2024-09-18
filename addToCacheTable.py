import json
import time
import boto3

def addToCacheTable(packId, packData):
    dynamodb = boto3.resource('dynamodb')
    tempTable = dynamodb.Table('fiori-cache-table')
    try:
        response = tempTable.update_item(
            Key={'packId': packId},
            UpdateExpression='SET packData = :packData, ttlExpiration = :ttlExpiration',
            ExpressionAttributeValues={':packData': packData, ':ttlExpiration': int(time.time() + 3600)}, # 1 hr
            ReturnValues="ALL_NEW"
        )
        print("added to cache table")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Added to CacheTable successfully',
                'updatedAttributes': response['Attributes']
            })
        }
    
    except Exception as e:
        print("failed adding to cache table")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error adding to CacheTable',
                'error': str(e)
            })
        }