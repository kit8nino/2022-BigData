from hdfs import Host, NameNode, Client

with open("Files/data.txt", encoding="utf-8") as f_:
    test_data = f_.read()

with open("Files/data2.txt", encoding="utf-8") as f_:
    test_data2 = f_.read()

with open("Files/data3.txt", encoding="utf-8") as f_:
    test_data3 = f_.read()

n_node = NameNode()
client = Client("User")
client.connect(n_node)
client.create_hosts(Host("host1", 14088), Host("host2", 31013), Host("host3", 20022))


file_name1 = "test.txt"
client.write_file(file_name1, test_data)

file_name2 = "test2.txt"
client.write_file(file_name2, test_data2)

file_name3 = "test3.txt"
client.write_file(file_name3, test_data3)


print(client.read_file(file_name1))
print(client.read_file(file_name2))
print(client.read_file(file_name3))

# удаление блоков хостов
# client.cleanup()
