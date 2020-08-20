import urllib.parse
import urllib.request

url = 'https://www.uniprot.org/uploadlists/'

batch_size = 1000


def individual_conversion(gene_batch):
    params = {
        'from': 'ACC+ID',
        'to': 'GENE+NAME',
        'format': 'tab',
        'query': ' '.join(gene_batch)
    }
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
    return response.decode('utf-8')


def do_conversion(genes):
    counter = 0
    gene_map = {}
    gene_length = len(genes)
    print("converting genes " + str(gene_length))
    while counter < gene_length:
        # TODO: this is a bug  as we need to conver the string
        # assert 0 == 1
        converted = individual_conversion(genes[counter:counter + batch_size])
        # print("converted: "+str(converted))
        for gene_entry in converted.split("\n"):
            gene_array = gene_entry.split("\t")
            if not gene_array[0].startswith("From", 0) and len(gene_array) > 1:
                gene_map[gene_array[0]] = gene_array[1]
        # return_genes
        # TODO: add to return genes
        counter += batch_size
        print("at : " + str(counter / gene_length * 100.0) + "%")

    return gene_map


def do_replace_genes(input_genes, conversion_map):
    output_genes = []
    for gene in input_genes:
        try:
            output_genes.append(conversion_map[gene.replace('UniProtKB:', '')])
        except:
            print("problem handling gene: " + gene)
            output_genes.append(individual_conversion([gene]))
    return output_genes


def convert_gmt_uniprots(input_file_name, conversion_map):
    output_file_name = input_file_name + "_converted.tsv"
    output_file = open(output_file_name, "w")
    print("writing to "+output_file_name)
    with open(input_file_name, "r") as a_file:
        for line in a_file:
            stripped_tabbed_line = line.strip().split("\t")
            gene_set_name = stripped_tabbed_line[0].split("%BP%")[0]
            gene_set_goid = stripped_tabbed_line[0].split("%BP%")[1]
            output_file.write(gene_set_name + "\t" + gene_set_goid + "\t")
            # print(str(stripped_tabbed_line))
            replaced_genes = do_replace_genes(input_genes=stripped_tabbed_line[1:], conversion_map=conversion_map)
            output_file.write(' '.join(replaced_genes) + "\n")
    output_file.close()


def get_genes_from_gmt(input_file_name):
    genes = []
    with open(input_file_name, "r") as a_file:
        for line in a_file:
            stripped_tabbed_line = line.strip().split("\t")
            genes.append(' '.join(stripped_tabbed_line[1:]).replace('UniProtKB:', '').strip().split(' '))
    return genes


# def build_db_uniprots(input_db, input_file_name):
#     with open(input_file_name, "r") as a_file:
#         for line in a_file:
#             stripped_tabbed_line = line.strip().split("\t")
#             output_line_str = ' '.join(stripped_tabbed_line[1:]).replace('UniProtKB:', '')
#             # output_genes = do_conversion(output_line_str)
#             for out_gene in output_genes.split("\n"):
#                 # formatted_genes = []
#                 if not out_gene.startswith("From", 0):
#                     tframe = out_gene.split("\t")
#                     if len(tframe) > 1:
#                         output_line_str += tframe[1] + " "
#             output_line_str += "\n"
#             # output_file.write(output_line_str)


print("GENE GENES\n")
genes = []
genes.extend(get_genes_from_gmt(input_file_name='test1.gmt'))
# genes.extend(get_genes_from_gmt(input_file_name='9606-bp-experimental.gmt'))
# genes.extend(get_genes_from_gmt(input_file_name='9606-bp-computational.gmt'))
# genes.extend(get_genes_from_gmt(input_file_name='9606-bp-all.gmt'))

flatten = lambda l: [item for sublist in l for item in sublist]
flattened = flatten(genes)
print("output flattened \n")

print("OUTPUT GENES\n")
print("gene sets: " + str(len(genes)))
print("gene list: " + str(len(flattened)))

unique_genes = list(set(flattened))
unique_genes.sort()

print("UNIQUE GENES: " + str(len(unique_genes)))

flattened_conversion_map = do_conversion(genes=unique_genes)

print("KEYS IN CONVERSION MAP: " + str(len(flattened_conversion_map.keys())))
# print(flattened_conversion_map)
# print("the key? -> " + " ".join(flattened_conversion_map.keys()))

convert_gmt_uniprots(input_file_name='test1.gmt', conversion_map=flattened_conversion_map)
# convert_gmt_uniprots(input_file_name='9606-bp-experimental.gmt', conversion_map=flattened_conversion_map)
# convert_gmt_uniprots(input_file_name='9606-bp-computational.gmt', conversion_map=flattened_conversion_map)
# convert_gmt_uniprots(input_file_name='9606-bp-all.gmt', conversion_map=flattened_conversion_map)
