class Node:
    def __init__ (self, data=None, next_node=None):
        self.data = data
        self.next_node = None

    def get_element (self):
        return self.data

    def set_element (self,d):
        self.data = None
    
    def set_next (self,n):
        self.next_node = n
        
    def get_next (self):
        return self.next_node

class Userclass:
    def __init__ (self):
        self.head = None

    def addfirst (self,item):
        new_element = Node(item)
        new_element.set_next(self.head)
        self.head = new_element

    def addlast (self,item):
        new_element = Node(item)
        if self.head is None:
            self.head = new_element
        last_element = self.head
        while last_element.next_node:
            last_element = last_element.next_node
        last_element.next_node = new_element

    def removefirst (self):
        while True:
            if self.head is None:
                print("\nERROR: Failed to remove an item!", end='')
                break
            self.head = self.head.next_node
            break

    def removelast (self):
        while True:
            count = self.count()
            if self.head is None:
                print("\nERROR: Failed to remove an item!", end='')
                break
            last_element = self.head
            while count > 2:
                last_element = last_element.next_node
                count -= 1
            last_element.next_node = None
            break

    def count(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.get_next()
        return count
    
    def forward(self):
        node = self.head
        print('')
        while node != None:
            print(node.data + ",", end='')
            node = node.next_node
        print('')

    def reverse(self):
        prev = None
        current = self.head
        while(current is not None):
            next_e = current.next_node
            current.next_node = prev
            prev = current
            current = next_e
        self.head = prev
        node = self.head
        print('')
        while node != None:
            print(node.data + ",", end='')
            node = node.next_node
        print('')

    def findMax(self):
        list = []
        node = self.head
        while node.next_node:
            list.append(int(node.data))
            node = node.next_node
        list.append(int(node.data))      
        print("\nMaximum number in the list: {}".format(max(list)))

    def findMin(self):
        list = []
        node = self.head
        while node.next_node:
            list.append(int(node.data))
            node = node.next_node
        list.append(int(node.data))
        print("\nMinimum number in the list: {}".format(min(list)))

    def printList(self):
        node = self.head
        print('')
        while node:
            print("[",node.data,"]","---> ", end='')
            node = node.next_node
        print('')

mylist = None
print('Welcome to linked list data structure!')
while True:    
    print('---------------------------------------------')
    print('Please choose what to do :')
    print('')
    print('1 = Create a new linked list')
    print('2 = Append to linked list')
    print('3 = Remove from linked list')
    print('4 = Count elements in linked list')
    print('5 = List the elements in linked list')
    print('6 = Find Max/Min number in linked list')
    print('7 = Print linked list')
    print('8 = Exit')
    print('---------------------------------------------')

    choice = input('Your choice : ')

    if choice == '1':
        mylist= Userclass()         
        print('\nLinked list created!')

    elif choice == '2':
        while True:
            if mylist == None:
                print("\nERROR: Please create a linked list first!")
                break            
            print('\n1 = Add to the beginning')
            print('2 = Add to the end')
            choice=input('\nYour choice : ')

            if choice == '1':
                add = input('\nAdd number : ')
                if add.isnumeric() == False:
                    print("\nERROR: Sorry, please enter a number!")
                    break
                mylist.addfirst(add)
            elif choice == '2':
                add = input('\nAdd number : ')
                if add.isnumeric() == False:
                    print("\nERROR: Sorry, please enter a number!")
                    break
                mylist.addlast(add)
            elif choice not in ['1','2']:
                print("\nERROR: Invalid input!")
                break

            print('\nAdd more numbers?(Y/N)')
            choice = input('\nYour choice : ')
            if choice not in ['Y', 'y']:
                break

    elif choice == '3':
        while True:
            if mylist == None:
                print("\nERROR: Please create a linked list first!")
                break        
            print('\n1 = Remove from the beginning')
            print('2 = Remove from the end')
            choice = input('\nYour choice : ')

            if choice == '1':
                mylist.removefirst()                
            elif choice == '2':                
                mylist.removelast()
            elif choice not in ['1','2']:
                print("\nERROR: Invalid input!")
                break

            if mylist.head == None:
                print("\nThe list is empty!")
                break
                        
            print('\nRemove more numbers?(Y/N)')
            choice=input('\nYour choice : ')
            if choice not in ['Y', 'y']:
                break

    elif choice == '4':
        while True:
            if mylist == None:
                print("\nERROR: Please create a linked list first!")
                break
            print('\nNumber of elements in the linked list: ',mylist.count())
            break

    elif choice == '5':
        while True:
            if mylist == None:
                print("\nERROR: Please create a linked list first!")
                break
            elif mylist.head == None:
                print("\nERROR: The list is empty!")
                break
            print('\n1 = List elements in forward order')
            print('2 = List elements in reverse order')
            choice = input('\nYour choice : ')
            if choice == '1':
                mylist.forward()            
            elif choice == '2':
                mylist.reverse()
            elif choice not in ['1','2']:
                print("\nERROR: Invalid input!")
                break
            break

    elif choice == '6':
        while True:
            if mylist == None:
                print("\nERROR: Please create a linked list first!")
                break
            elif mylist.head == None:
                print("\nERROR: The list is empty!")
                break
            print('\n1 = Find maximum number')
            print('2 = Find minimum number')
            choice = input('\nYour choice : ')
            if choice == '1':
                mylist.findMax()
            elif choice == '2':
                mylist.findMin()
            elif choice not in ['1','2']:
                print("\nERROR: Invalid input!")
                break
            break
    
    elif choice == '7':
        while True:
            if mylist == None:
                print("\nERROR: Please create a linked list first!")
                break
            elif mylist.head == None:
                print("\nERROR: The list is empty!")
                break
            print("\nList of element(s):")
            mylist.printList()
            break
        
    elif choice == '8':
        print("\nYou have exited!")
        break

    else:
        print("\nERROR: Invalid input!")
