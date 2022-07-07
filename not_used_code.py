
import pickle

if __name__ == '__main__':
    with open('shoplistfile.bin', 'wb') as file:
        pickle.dump([ 'Помидоры','Шоколад','Апельсины' ], file)

    with open('shoplistfile.bin', 'rb') as file:
         shoplist_info = pickle.load(file)
         print(shoplist_info)



