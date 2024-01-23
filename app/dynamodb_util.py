import boto3


class DynamoDBUtil:

    def __init__(self, table_name, pk_name):
        self.table_name = table_name
        self.pk_name = pk_name

        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(self.table_name)

        self.table.load()

    def save(self, item):
        self.table.put_item(Item=item)

    def get(self, pk):
        response = self.table.get_item(
            Key={
                self.pk_name: pk
            }
        )
        return response["Item"] if response else None




