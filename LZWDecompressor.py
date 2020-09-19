from bitstream import BitStream


def load_in(file_name, fixed_width_length):
    with open(file_name, 'rb') as f: 
        file_content = f.read() 
        
        #Get input as stream of bits and split by 12
        bit_stream_as_string = str(BitStream(file_content))
        
        #If odd get last code
        odd = False
        if len(bit_stream_as_string) % fixed_width_length != 0:
            last_code = int(bit_stream_as_string[-fixed_width_length:], 2)
            bit_stream_as_string = bit_stream_as_string[:-16]
            odd = True
            
        code_array = [bit_stream_as_string[i:i+fixed_width_length] for i in range(0, len(bit_stream_as_string), fixed_width_length)]

        #Convert to codes
        for i in range(0, len(code_array)):
            code_array[i] = int(code_array[i],2)
        if odd:
            code_array.append(last_code)

        return code_array

def initialise_dict():
    dictionary = {}
    for n in range(0,256):
        dictionary[n] = chr(n)
    return dictionary

def decompress(code_array, fixed_width_length):
    #Decompression algorithm
    output_sequence = ''
    new_addition = ''
    conjecture = None
    
    dictionary = initialise_dict()

    for code in code_array:
            if code in dictionary:
                output_sequence = output_sequence + dictionary[code]
                
                #Reset if out of codes
                if len(dictionary) == pow(2, fixed_width_length):
                    dictionary = initialise_dict()
                    
                if conjecture is not None:
                    #Create and add new dictionary item at new code
                    new_addition = conjecture + dictionary[code][0]
                    dictionary[len(dictionary)] = new_addition
                    
                conjecture = str(dictionary[code])
                
            else:
                #Special case
                new_addition = conjecture + conjecture[0]
                output_sequence = output_sequence + new_addition
                dictionary[len(dictionary)] = new_addition

    return output_sequence

fixed_width_length = 12
file_name = "./LzwInputData/compressedfile4.z"
codes = load_in(file_name, fixed_width_length)
decompressed_string = decompress(codes, fixed_width_length)
print(decompressed_string)


