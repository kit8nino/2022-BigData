from hdfs import Host, NameNode, Client

with open("test/test_1.txt", encoding="utf-8") as f_:
    test_test_1 = f_.read()
with open("test/test_2.txt", encoding="utf-8") as f_:
    test_test_2 = f_.read()
with open("test/test_3.txt", encoding="utf-8") as f_:
    test_test_3 = f_.read()

n_node = NameNode()
client = Client("Keksik")
client.connect(n_node)
client.create_hosts(Host("simple_host_1", 15000),
                    Host("simple_host_2", 15000),
                    Host("simple_host_3", 15000),
                    Host("simple_host_4", 15000))

file_name1 = "TEST_1.txt"
client.write_file(file_name1, test_test_1)
file_name2 = "TEST_2.txt"
client.write_file(file_name2, test_test_2)
file_name3 = "TEST_3.txt"
client.write_file(file_name3, test_test_3)

print(client.read_file(file_name1))
print(client.read_file(file_name2))
print(client.read_file(file_name3))