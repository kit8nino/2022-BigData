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

HOST_1 = Host("REPLICA_HOST_1", 15000)
HOST_2 = Host("REPLICA_HOST_2", 15000)
HOST_3 = Host("REPLICA_HOST_3", 15000)
HOST_4 = Host("REPLICA_HOST_4", 15000)

# Создадим 4 хоста
client.create_hosts(HOST_1, HOST_2, HOST_3, HOST_4)
# Заполним данными и проверим
file_name = "TEST_1.txt"
client.write_file(file_name, TEST_DATA_1)
client.write_file(file_name, TEST_DATA_2)
client.write_file(file_name, TEST_DATA_3)
res = client.read_file(file_name)
print("\n\n==========ПРОВЕРКА 1==========\n")
print(res + "\n")

# Все хосты, кроме третьего вышли из строя. Третий хост последняя надежда
HOST_1.is_alive = False
HOST_2.is_alive = False
#HOST_3.is_alive = False <--
HOST_4.is_alive = False
res = client.read_file(file_name)
print("\n\n=========ПРОВЕРКА 2==========\n")
print(res + "\n")


# Все хосты вышли из строя
HOST_1.is_alive = False
HOST_2.is_alive = False
HOST_3.is_alive = False
HOST_4.is_alive = False
res = client.read_file(file_name)
print("\n\n==========ПРОВЕРКА 3==========\n")
print(res)
