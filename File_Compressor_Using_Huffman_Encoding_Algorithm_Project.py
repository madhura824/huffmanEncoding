import heapq
import os

class BinaryTree:
    def __init__(self,value,freq):
        self.value=value
        self.freq=freq
        self.left_node=None
        self.right_node=None
    def __lt__(self,other):  
        return self.freq<other.freq

    def __eq__(self,other):
        return self.freq==other.freq
        
        
class Huffmancode:
    def __init__(self,path=None):
        self.path=path
        self.__nodes_list=[]
        self.__code_dict={}
        self.__reverse_code_dict={}
    #our __nodes_list has BinaryTree object having 4 values and heapify will not know on what basis to heapify therefore we are using thses two functions
    
    
    def __frequency_from_text(self, text):   # __ double dash before the fun name / var name states that it is private
        freq_dict={}

        for char in text:
            if char not in freq_dict:
                freq_dict[char]=0
            else:
                freq_dict[char]+=1
        return freq_dict
    
    def __Build_Heap(self,freq_dict):
        for key in freq_dict:
            value=freq_dict[key]
            node = BinaryTree(key,value)  #create a node (object) using the constructor of BinaryTree
            heapq.heappush(self.__nodes_list,node) #pushes the node in  the nodes list which s a normal list
    
    def Build_Binary_Tree(self):
        #creates BinaryTree object for every character   
        while len(self.__nodes_list)>1:
            
    
            Node1=heapq.heappop(self.__nodes_list)
            Node2=heapq.heappop(self.__nodes_list)
            sum_of_freq=Node1.freq+Node2.freq
            New_Node=BinaryTree(None,sum_of_freq)
            New_Node.left_node=Node1
            New_Node.right_node=Node2
            heapq.heappush(self.__nodes_list,New_Node)
        return 
    
    def Build_Tree_Code_Helper(self,root,current_code):
        if root is None:
            return
        if root.value is not None:
            self.__code_dict[root.value]=current_code
            self.__reverse_code_dict[current_code]=root.value
        self.Build_Tree_Code_Helper(root.left_node,current_code+'0')
        self.Build_Tree_Code_Helper(root.right_node,current_code+'1')
        
        return 
    
    def Build_Tree_Code(self):
        root=heapq.heappop(self.__nodes_list)
        self.Build_Tree_Code_Helper(root,'')
        
    def Create_Encoded_Text(self,text):
        Encoded_Text=''
        for char in text:
            Encoded_Text+=self.__code_dict[char]
         
        return Encoded_Text
    def Add_Padding_to_EncodedText(self,Encoded_Text):
        no_of_padding_bits=8-len(Encoded_Text)%8
        
        for i in range (no_of_padding_bits):
            Encoded_Text+='0'
        padded_info = "{0:08b}".format(no_of_padding_bits) 
        #0 befre decimal gives the index of arguument that we have to work
        #here we have only one argument
         #.08b after decimal tells us that we have to convert the value of the argument i.e no_of_padding_bits into a 8 bit binary format
        padded_text=padded_info+Encoded_Text
        
        return padded_text
    
    def __Build_Byte_Array(self, padded_text):
        byte_array=[]
        for i in range(0,len(padded_text),8):
            byte=padded_text[i:i+8]
            byte_array.append(int(byte,2))  #integer form of the byyte which is in base 2 form i.e. binary form
        return byte_array
    def Compression(self):
        
        #access the file extract the text from the file
        filename,fileextension = os.path.splitext(self.path)
        outputpath=filename+'.bin'  #output file is of type binary
        
        with open(self.path,'r+') as file, open(outputpath,'wb') as output:  #wb - write binary
            text=file.read()
            text=text.rstrip()  #removes extra spaecs from text
            
            #create a frequency dictionary and store freq of every character
            freq_dict=self.__frequency_from_text(text)


            # create a min heap and push all the nodes into the min heap (node : value, freq, left node , right node)

            nodes_heap= self.__Build_Heap(freq_dict)
            #build the binary tree
            self.Build_Binary_Tree()
            #construct code from the binary tree and store it into the dictionary
            self.Build_Tree_Code()
            #construct encoded text and return it as the output
            Encoded_Text=  self.Create_Encoded_Text(text)
            #Add padding to the encodeed text
            padded_text=self.Add_Padding_to_EncodedText(Encoded_Text)

            #Build byte array divide the paddedtext in 8 bits convert it to decimal, push it to array

            byte_array=self.__Build_Byte_Array(padded_text)
            final_bytes=bytes(byte_array)   #creates immutable sequence of bytes (data is not modified and ensures that it cannot be modified)
            output.write(final_bytes)
            print("compressed successfully")
            return outputpath
    
    def __Remove_Padding(self,text):
        padding_info=text[:8]
        padding_value=int(padding_info,2)
        text=text[8:]
        text=text[:-1*padding_value]
        return text
    def __Decode_Text(self, text):
        decoded_text = ''
        current_string = ''
        for char in text:
            current_string += char
            if current_string in self.__reverse_code_dict:
                character = self.__reverse_code_dict[current_string]
                decoded_text += character
                current_string = ''
        print("Decoded Text (Inside __Decode_Text):", decoded_text)
        return decoded_text
        
        
    
    def Decompress(self, input_path):  #inputpath /output path is the file_name  abc.txt
        filename, file_extension = os.path.splitext(input_path)
        complete_file_name=filename+'.bin'
        output_path=filename+'_decompressed'+'.txt'
        with open(complete_file_name,'rb') as file ,open(output_path, 'w') as output:
            bit_string=''
            byte=file.read(1) #read 1 byte from the compreseed file
            #when we read the byte from the compressed file, it is in hex form 0x bd6556
            while byte:
                byte=ord(byte)  # convert it to integer using ord()
                bits=bin(byte)[2:].rjust(8,'0') #convert the integer into binary format which looks like b' 01001
                #now in this b'01001 we dont want b' therefore we do slicing [2:]
                #rjust converts the binary no eg 011 in 8 bits 0000 0011
                
                bit_string+=bits
                
                byte=file.read(1)
            print("Bit String:", bit_string)
            text_after_removing_padding=self.__Remove_Padding(bit_string)
            print("Text After Removing Padding:", text_after_removing_padding)
            decoded_text=self.__Decode_Text(text_after_removing_padding)
            print("Decoded Text:", decoded_text)
            output.write(decoded_text)
            print('Decompressed Successfully')
        return
# path=input('Enter the path of file which you need to encode: ')
# h=Huffmancode(path)
# compressed_file=h.Compression()

# h.Decompress(compressed_file)
