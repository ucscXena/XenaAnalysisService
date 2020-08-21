import sys
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


def do_conversion(input_genes):
    counter = 0
    gene_map = {}
    gene_length = len(input_genes)
    print("converting genes " + str(gene_length))
    while counter < gene_length:
        converted = individual_conversion(input_genes[counter:counter + batch_size])
        for gene_entry in converted.split("\n"):
            gene_array = gene_entry.split("\t")
            if not gene_array[0].startswith("From", 0) and len(gene_array) > 1:
                gene_map[gene_array[0]] = gene_array[1]
        counter += batch_size
        print("at : " + str(counter / gene_length * 100.0) + "%")

    return gene_map


def do_replace_genes(input_genes, conversion_map):
    output_genes = []
    for gene in input_genes:
        try:
            output_genes.append(conversion_map[gene.replace('UniProtKB:', '')])
        except:
            print("problem handling gene: " + gene + " so ignoring")
            # output_genes.append(individual_conversion([gene]))
    return output_genes


def convert_gmt_uniprots(input_file_name, conversion_map):
    output_file_name = input_file_name + "_converted.tsv"
    output_file = open(output_file_name, "w")
    print("writing to " + output_file_name)
    with open(input_file_name, "r") as a_file:
        for line in a_file:
            stripped_tabbed_line = line.strip().split("\t")
            gene_set_name = stripped_tabbed_line[0].split("%BP%")[0]
            gene_set_goid = stripped_tabbed_line[0].split("%BP%")[1]
            output_file.write(gene_set_name + "\t" + gene_set_goid + "\t")
            replaced_genes = do_replace_genes(input_genes=stripped_tabbed_line[1:], conversion_map=conversion_map)
            output_file.write('\t'.join(replaced_genes) + "\n")
    output_file.close()


def get_genes_from_gmt(input_file_name):
    retrieved_genes = []
    with open(input_file_name, "r") as a_file:
        for line in a_file:
            stripped_tabbed_line = line.strip().split("\t")
            retrieved_genes.append(' '.join(stripped_tabbed_line[1:]).replace('UniProtKB:', '').strip().split(' '))
    return retrieved_genes


print("input arguments: " + str(sys.argv))
if len(sys.argv) < 2:
    print("exiting, need file argument")
    exit(1)

input_gmt_file = sys.argv[1]
print("converting gmt file: " + input_gmt_file)

print("GENE GENES\n")
genes = []
genes.extend(get_genes_from_gmt(input_file_name=input_gmt_file))

flatten = lambda l: [item for sublist in l for item in sublist]
flattened = flatten(genes)

print("OUTPUT GENES")
print("gene sets: " + str(len(genes)))
print("gene list: " + str(len(flattened)))

unique_genes = list(set(flattened))
unique_genes.sort()

print("UNIQUE GENES: " + str(len(unique_genes)))

flattened_conversion_map = do_conversion(input_genes=unique_genes)

print("KEYS IN CONVERSION MAP: " + str(len(flattened_conversion_map.keys())))

convert_gmt_uniprots(input_file_name=input_gmt_file, conversion_map=flattened_conversion_map)
