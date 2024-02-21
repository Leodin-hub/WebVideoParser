from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer

admin = KafkaAdminClient(bootstrap_servers="localhost:9092")
admin.delete_topics()

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
consumer = KafkaConsumer('decode', group_id='group2', bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest')

# for i in range(10):
#     producer.send('stream', bytes(str(i), 'utf-8'))

while True:
    i = consumer.__next__()
    if i:
        print(i.value.decode('utf-8'))
