from hdfs import Host, NameNode, Client

with open("Files/data_1.txt", encoding="utf-8") as f_:
    data1 = f_.read()

with open("Files/data_2.txt", encoding="utf-8") as f_:
    data2 = f_.read()

with open("Files/data_3.txt", encoding="utf-8") as f_:
    data3 = f_.read()

with open("Files/data_4.txt", encoding="utf-8") as f_:
    data4 = f_.read()

n_node = NameNode()
client = Client("User")
client.connect(n_node)
client.create_hosts(Host("host1", 59219), Host("host2", 15756), Host("host3", 13452), Host("host4", 24542))


file_name1 = "[1]data.txt"
client.write_file(file_name1, data1)

file_name2 = "[2]data.txt"
client.write_file(file_name2, data2)

file_name3 = "[3]data.txt"
client.write_file(file_name3, data3)

file_name4 = "[4]data.txt"
client.write_file(file_name4, data4)



print(client.read_file(file_name1))
print(client.read_file(file_name2))
print(client.read_file(file_name3))
print(client.read_file(file_name4))


