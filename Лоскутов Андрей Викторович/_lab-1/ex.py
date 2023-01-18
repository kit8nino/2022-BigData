from hdfs import Host, NameNode, Client

with open("1.txt", encoding="utf-8") as f_:
    test_data1 = f_.read()
with open("2.txt", encoding="utf-8") as f_:
    test_data2 = f_.read()
with open("3.txt", encoding="utf-8") as f_:
    test_data3 = f_.read()

n_node = NameNode()
client = Client("user")
client.connect(n_node)
client.create_hosts(Host("host1", 10000), Host("host2", 11000), Host("host3", 12000))

file1 = "1.txt"
client.write_file(file1, test_data1)
file2 = "2.txt"
client.write_file(file2, test_data2)
file3 = "3.txt"
client.write_file(file3, test_data3)

print(client.read_file(file1))
print(client.read_file(file2))
print(client.read_file(file3))