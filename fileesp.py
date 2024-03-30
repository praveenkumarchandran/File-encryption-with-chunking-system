import os

def split_file(input_file, output_dir):
    # Create output directory if it doesn't exist
    filepath = input_file
    head, tail = os.path.split(filepath)
    print(head)
    #if not os.path.exists(output_dir):
        #os.makedirs(output_dir)

    # Get the size of the input file
    file_size = os.path.getsize(input_file)

    # Calculate the chunk size for each part
    chunk_size = file_size // 4

    # Open input file in binary mode
    with open(input_file, 'rb') as f:
        for i in range(4):
            # Create output file for the current part
            output_file = os.path.join( head+"/split/"+f'{i + 1}'+tail)
            print(output_file)
            with open(output_file, 'wb') as part:
                # Read a chunk of data and write it to the output file
                chunk = f.read(chunk_size)
                part.write(chunk)


input_file = "static/upload/277Chrysanthemum.jpg"
output_dir = ""

split_file(input_file, output_dir)