from hdfs_simulation import Host, NameNode, Client

with open("assets/test_data3.txt", encoding="utf-8") as f_:
    test_data = f_.read()


n_node = NameNode()
client = Client("user")
client.connect(n_node)

host1 = Host("host1", 12800)
host2 = Host("host2", 25600)
host3 = Host("host3", 45000)
host4 = Host("host4", 12800)
client.create_hosts(host1, host2, host3, host4)

file_name = "test3.txt"
client.write_file(file_name, test_data)


res = client.read_file(file_name)
print(res + "\n")


host1.is_alive = False
res = client.read_file(file_name)
print(res + "\n")



host2.is_alive = False
host3.is_alive = False
host4.is_alive = False
res = client.read_file(file_name)
print(res)