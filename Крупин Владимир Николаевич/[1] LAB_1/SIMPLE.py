from HDFS import Host, NameNode, Client

with open("DATES/DATA_1.txt", encoding="utf-8") as f_:
    TEST_DATA_1 = f_.read()
with open("DATES/DATA_2.txt", encoding="utf-8") as f_:
    TEST_DATA_2 = f_.read()
with open("DATES/DATA_3.txt", encoding="utf-8") as f_:
    TEST_DATA_3 = f_.read()

n_node = NameNode()
client = Client("GRIBABAS")
client.connect(n_node)
client.create_hosts(Host("SIMPLE_HOST_1", 15000), Host("SIMPLE_HOST_2", 15000), Host("SIMPLE_HOST_3", 15000), Host("SIMPLE_HOST_4", 15000))

file_name1 = "TEST_1.txt"
client.write_file(file_name1, TEST_DATA_1)
file_name2 = "TEST_2.txt"
client.write_file(file_name2, TEST_DATA_2)
file_name3 = "TEST_3.txt"
client.write_file(file_name3, TEST_DATA_3)

print(client.read_file(file_name1))
print(client.read_file(file_name2))
print(client.read_file(file_name3))


