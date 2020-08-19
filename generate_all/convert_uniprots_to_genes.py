import urllib.parse
import urllib.request

url = 'https://www.uniprot.org/uploadlists/'


def do_conversion(genes):
    params = {
        'from': 'ACC+ID',
        'to': 'GENE+NAME',
        'format': 'tab',
        'query': genes
    }
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
        response = f.read()
    return response.decode('utf-8')


def convert_gmt_uniprots(input_file_name):
    output_file_name = input_file_name + "_converted.tsv"
    output_file = open(output_file_name, "w")
    with open(input_file_name, "r") as a_file:
        for line in a_file:
            stripped_tabbed_line = line.strip().split("\t")
            gene_set_name = stripped_tabbed_line[0].split("%BP%")[0]
            gene_set_goid = stripped_tabbed_line[0].split("%BP%")[1]
            print("Processing: " + gene_set_name)
            output_file.write(gene_set_name + "\t" + gene_set_goid + "\t")
            output_line_str = ' '.join(stripped_tabbed_line[1:]).replace('UniProtKB:', '')
            output_genes = do_conversion(output_line_str)
            for out_gene in output_genes.split("\n"):
                # formatted_genes = []
                if not out_gene.startswith("From", 0):
                    tframe = out_gene.split("\t")
                    if len(tframe) > 1:
                        output_line_str += tframe[1] + " "
            output_line_str += "\n"
            output_file.write(output_line_str)


convert_gmt_uniprots(input_file_name='9606-bp-experimental.gmt')
