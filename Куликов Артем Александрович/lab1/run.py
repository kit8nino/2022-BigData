from main import Host, NameNode, Client

with open("text/text.txt", encoding="utf-8") as f_:
    test_data = f_.read()

with open("text/text1.txt", encoding="utf-8") as f_:
    test_data2 = f_.read()

with open("text/text2.txt", encoding="utf-8") as f_:
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


file_name1 = "text.txt"
client.write_file(file_name1, test_data)
print(client.read_file(file_name1))

file_name2 = "text1.txt"
client.write_file(file_name2, test_data2)
print(client.read_file(file_name2))

file_name3 = "text2.txt"
client.write_file(file_name3, test_data3)
res = client.read_file(file_name3)
print(res + "\n")

host3.is_alive = False
res = client.read_file(file_name3)
print(res + "\n")
