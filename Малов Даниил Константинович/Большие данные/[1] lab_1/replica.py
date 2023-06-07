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

host_1 = Host("replica_host_1", 15000)
host_2 = Host("replica_host_2", 15000)
host_3 = Host("replica_host_3", 15000)
host_4 = Host("replica_host_4", 15000)

# Создадие хостов
client.create_hosts(host_1, host_2, host_3, host_4)

# Заполним данными и проверим
file_name = "TEST_1.txt"
client.write_file(file_name, test_test_1)
client.write_file(file_name, test_test_2)
client.write_file(file_name, test_test_3)
res = client.read_file(file_name)
print("\n==========Проверка 1==========\n")
print(res + "\n")

# Все хосты, кроме третьего вышли из строя
host_1.is_alive = False
host_2.is_alive = False

#HOST_3.is_alive = False <--
host_4.is_alive = False
res = client.read_file(file_name)
print("\n=========Проверка 2==========\n")
print(res + "\n")

# Все хосты вышли из строя
host_1.is_alive = False
host_2.is_alive = False
host_3.is_alive = False
host_4.is_alive = False
res = client.read_file(file_name)
print("\n==========Проверка 3==========\n")
print(res)