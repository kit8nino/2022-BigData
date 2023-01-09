from HDFS import Host, NameNode, Client

with open("test/test1.txt", encoding="utf-8") as f_:
    test_data = f_.read()

with open("test/test2.txt", encoding="utf-8") as f_:
    test_data2 = f_.read()

with open("test/test3.txt", encoding="utf-8") as f_:
    test_data3 = f_.read()

n_node = NameNode()
client = Client("user")
client.connect(n_node)
host1 = Host("host1", 12800)
host2 = Host("host2", 25600)
host3 = Host("host3", 12800)
host4 = Host("host4", 25600)
host5 = Host("host5", 51200)
host6 = Host("host6", 6400)
hosts = [host1,host2]
client.create_hosts(hosts)
hosts1 = [host3,host4,host5,host6]
client.create_hosts(hosts1)

client.write_file("data1.txt", test_data)
print(client.read_file("data1.txt"))

client.write_file("data2.txt", test_data2)      
print(client.read_file("data2.txt"))

client.write_file("data3.txt", test_data3)
res = client.read_file("data3.txt")
print(res + "\n")

host3.is_alive = False
res = client.read_file("data3.txt")
print(res + "\n")