rule ungzip_file:
	input:
		"nanopore_output/{fileName}.fastq.gz"
	output:
		"ungzipped_files/{fileName}.fastq"
	shell:
		"gzip -d -k -c {input} > {output}"
		
rule run_kraken:
	input:
		"ungzipped_files/{fileName}.fastq"
	output:
		"kraken_results/{fileName}.kraken2"
	shell:
		"kraken2 --db /home/bioinf/kraken8db --memory-mapping {input} > {output}"
