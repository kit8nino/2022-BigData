from lab1 import Host, NameNode, Client

n_node = NameNode()
client = Client("user")
client.connect(n_node)
client.create_hosts(Host("host1", 10000), Host("host2", 11000), Host("host3", 12000))
file_name = ["test1.txt","test2.txt","test3.txt"]
test_data = []

for i in range(len(file_name)):
    with open(file_name[i], encoding="utf-8") as f_:
        test_data.append(f_.read())

for i in range(len(file_name)):
    client.write_file(file_name[i], test_data[i])

for i in range(len(file_name)):
    print(client.read_file(file_name[i]))

input()