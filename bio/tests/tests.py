#!/home/edario/mines/bio/bin/python3

from Bio import Entrez

Entrez.email = "ram.le.dario@gmail.com"

import sys
import os
import subprocess
from datetime import datetime

from Bio import SeqIO
import ray
# parser=argparse.ArgumentParser()
# verbose=False

nproc=int(subprocess.check_output("""lscpu | grep 'CPU(s):' | head -1 | awk '{print $2}'""",shell=True))
# av_mem=int(subprocess.check_output("free | grep Mem | awk '{print $2-$3}'",shell=True))

# ray.init()

# @ray.remote(num_cpus=nproc)
# def dummy():
# 	print("Available memory for this device: %i bytes" % av_mem)

# id=dummy.remote()
# ray.get(id)
# quit()

def __parse_args__():
	# global parser, verbose
	# global verbose
	import argparse
	parser=argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', help='TO-DO', action='store_true')
	'''
	Increasing retmax allows more of the retrieved UIDs to be included in the XML output, up to a maximum 
	of 100,000 records. To retrieve more than 100,000 UIDs, submit multiple esearch requests while 
	incrementing the value of retstart.

	Taken from: https://www.ncbi.nlm.nih.gov/books/NBK25499/
	'''
	parser.add_argument('-rm', '--retmax', help='Total number of UIDs from the retrieved set to be shown in the XML output', type=int)

	parser.add_argument('-t', '--tool', help='Support for clustalo, clustalw, muscle, emboss, tcoffee, blast [default: clustalo]', type=str, default="clustalo")
	parser.add_argument('-if', '--input-file', help='TO-DO', type=str)
	parser.add_argument('-fif', '--file-input-format', help='TO-DO', type=str)
	parser.add_argument('-fof', '--file-output-format', help='Used by MUSCLE; valid values: empty|none (FASTA, by default), clustal and clustal-strict', type=str)
	parser.add_argument('-ea', '--emboss-algorithm', help='Used by EMBOSS; valid values: water (Smith-Waterman algorithm for local alignment) and needle (Needleman-Wunsch algorithm for global alignment) [default: needle]', type=str, default="needle")
	parser.add_argument('-tct', '--t-coffee-tool', help='UNIMPLEMENTED! Used by t_coffee; valid values: [default: ?]', type=str, default=None)
	parser.add_argument('-ur', '--using-ray', help='Use ray for run in distributed environment [default: false]', action='store_true')
	parser.add_argument('-bap', '--blast-app', help='Currently qblast only works with blastn, blastp, blastx, tblast and tblastx', type=str, default=None)
	parser.add_argument('-bdb', '--blast-database', help='The databases to search against. The options for this are available on the NCBI Guide to BLAST ftp://ftp.ncbi.nlm.nih.gov/pub/factsheets/HowTo_BLASTGuide.pdf', type=str, default=None)
	# parser.add_argument('-bqs', '--blast-query-sequence', help=' A string containing your query sequence. This can either be the sequence itself, the sequence in fasta format, or an identifier like a GI number', type=str, default=None)

	args = parser.parse_args()

	# verbose=args.verbose
	# args.tool="clustalo"
	# args.using_ray=False

	return args

def __retrieve_data__(args=None):
	assert args is not None, "Missed the args at __retrieve_data__(args=None)"
	assert args.retmax is not None, "Missed the arg -rm|--retmax at __retrieve_data__(args=None)"
	assert args.retmax>0, "The arg -rm|--retmax must be greater than zero"

	if args.verbose:
		print("Retrieving data...\n")
		started=datetime.now()
		print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))

	# record=[]
	handle = Entrez.esearch(db="nucleotide", retmax=args.retmax, term="SARS-CoV-2")
	record = Entrez.read(handle)
		# if args is not None and args.verbose:

	if args.verbose:
		print("Finished the data retrieving process")
		finished=datetime.now()
		print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
		print("Total elapsed time: %s" % str(finished-started))
		print("Data retrieved is:\n")
		print(record)
		# return record["IdList"]

	return record

def __fetch_seqs__(args=None,ids=None):
	assert args is not None, "Missed the args at __fetch_seqs__(args=None,ids=None)"
	assert ids is not None, "Missed the ids at __fetch_seqs__(args=None,ids=None)"

	if args.verbose:
		print("\nRetrieving sequences...\n")
		started=datetime.now()
		print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))

	seqs=[]

	# import os
	fout=open("tmp.fasta",'w')

	for id in ids:
		handle = Entrez.efetch(db="nucleotide", id=id, rettype="fasta", retmode="text")
		record = handle.read()
		fout.write(record)
		handle.close()
		seqs.append(record)
		# print(record)

	fout.close()

	if args.verbose:
		print("Finished the sequences retrieving process")
		finished=datetime.now()
		print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
		print("Total elapsed time: %s" % str(finished-started))
		print("\nAccesions (IDs) retrieved:\n")
		from Bio.SeqRecord import SeqRecord
		for seq in SeqIO.parse("tmp.fasta","fasta"):
			print(seq.id)
		# print(seqs)

	return seqs

def __align_sequences__(args=None,seqs=None):
	if args.input_file is not None:
		assert args.file_input_format is not None, "Missed the file input format at __retrieve_data__(args=None)"

		if args.verbose:
			print("\nStarting sequences alignment process...\n\n")
		
		from Bio.Align import Applications
		# import subprocess
		# global nproc

		if args.tool=="clustalo":
			started=datetime.now()
			print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))
			# from Bio.Align.Applications import ClustalwCommandline
			binpath=r"/usr/local/bin/clustalo"
			cmd=Applications.ClustalOmegaCommandline(\
				binpath,\
				infile=args.input_file,\
				outfile="%s.aln.clustalo" % args.input_file,\
				verbose=args.verbose,\
				force=True,\
				threads=nproc,\
				guidetree_out="%s.dnd.clustalo" % args.input_file)
			# cmd="%s -i %s -o %s --threads=%i --force --guidetree-out=%s" % (binpath, args.input_file, ("%s.aln.clustalo" % args.input_file), nproc, ("%s.dnd.clustalo" % args.input_file))
			# if args.verbose:
			# 	cmd="%s -i %s -o %s --threads=%i --force --guidetree-out=%s -v" % (binpath, args.input_file, ("%s.aln.clustalo" % args.input_file), nproc, ("%s.dnd.clustalo" % args.input_file))
			# stdout,stderr=cmd()
			child=subprocess.Popen(\
				str(cmd),\
				stdout=subprocess.PIPE,\
				stderr=subprocess.PIPE,\
				universal_newlines=True,\
				shell=(sys.platform!="win32"))
			child.wait()
			finished=datetime.now()
			print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
			print("Total elapsed time: %s" % str(finished-started))
			if args.verbose:
				stdout=child.stdout.read()
				if (len(stdout)>0):
					print("\nStandard out is: %s\n" % stdout)
				else:
					print("\nStandard out is empty!\n")

				stderr=child.stderr.read()
				if (len(stderr)>0):
					print("Standard error is: %s" % stderr)
				else:
					print("Standard error is empty")

			from Bio import AlignIO
			# align=AlignIO.read("tmp.aln","fasta")
			align=AlignIO.read("%s.aln.clustalo" % args.input_file,"fasta")
			print(align)
		elif args.tool=="muscle":
			started=datetime.now()
			print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))
			# from Bio.Align.Applications import ClustalwCommandline
			cmd=None
			if not args.file_output_format or args.file_output_format is None:
				cmd=Applications.MuscleCommandline(input=args.input_file,out="%s.aln.muscle" % args.input_file)
			else:
				if args.file_output_format=="clustal":
					cmd=Applications.MuscleCommandline(input=args.input_file,clw=True,out="%s.aln.muscle.clustalwfmt" % args.input_file)
				elif args.file_output_format=="clustal-strict":
					cmd=Applications.MuscleCommandline(input=args.input_file,clwstrict=True,out="%s.aln.muscle.clustalwstrictfmt" % args.input_file)
			# cmd()
			child=subprocess.Popen(\
				str(cmd),\
				stdout=subprocess.PIPE,\
				stderr=subprocess.PIPE,\
				universal_newlines=True,\
				shell=(sys.platform!="win32"))
			child.wait()
			finished=datetime.now()
			print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
			print("Total elapsed time: %s" % str(finished-started))
			if args.verbose:
				stdout=child.stdout.read()
				if (len(stdout)>0):
					print("\nStandard out is: %s\n" % stdout)
				else:
					print("\nStandard out is empty!\n")

				stderr=child.stderr.read()
				if (len(stderr)>0):
					print("Standard error is: %s" % stderr)
				else:
					print("Standard error is empty")

			from Bio import AlignIO
			align=None
			if args.file_output_format is None:
				align=AlignIO.read("%s.aln.muscle" % args.input_file,"fasta")
			elif args.file_output_format=="clustal":
				align=AlignIO.read("%s.aln.muscle.clustalwfmt" % args.input_file,"clustal")
			elif args.file_output_format=="clustal-strict":
				align=AlignIO.read("%s.aln.muscle.clustalwstrictfmt" % args.input_file,"clustal")
			print(align)
		elif args.tool=="emboss":
			raise NotImplementedError("Not implemented yet! Fix the a and b sequence files")
			outfile=''
			binpath=''
			if args.emboss_algorithm=="needle":
				from Bio.Emboss.Applications import NeedleCommandline as EmbossCommandline
				outfile="%s.needle.txt" % args.input_file
				binpath=r"/usr/local/bin/needle"
			elif args.emboss_algorithm=="water":
				from Bio.Emboss.Applications import WaterCommandline as EmbossCommandline
				outfile="%s.water.txt" % args.input_file
				binpath=r"/usr/local/bin/water"
			started=datetime.now()
			print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))
			cmd=EmbossCommandline(\
				binpath,\
				asequence="/home/edario/mines/bio/alpha.faa",\
				bsequence="/home/edario/mines/bio/beta.faa",\
				gapopen=10,\
				gapextend=0.5,\
				outfile=outfile)
			# stdout,stderr=cmd()
			child=subprocess.Popen(\
				str(cmd),\
				stdout=subprocess.PIPE,\
				stderr=subprocess.PIPE,\
				universal_newlines=True,\
				shell=(sys.platform!="win32"))
			child.wait()
			finished=datetime.now()
			print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
			print("Total elapsed time: %s" % str(finished-started))
			if args.verbose:
				stdout=child.stdout.read()
				if (len(stdout)>0):
					print("\nStandard out is: %s\n" % stdout)
				else:
					print("\nStandard out is empty!\n")

				stderr=child.stderr.read()
				if (len(stderr)>0):
					print("Standard error is: %s" % stderr)
				else:
					print("Standard error is empty")

			from Bio import AlignIO
			# align=AlignIO.read("tmp.aln","fasta")
			# align=AlignIO.read("%s.needle.txt" % args.input_file,"emboss")
			align=AlignIO.read(outfile,"emboss")
			print(align)
		elif args.tool=="blast":
			assert args.blast_app is not None, "Missed the -bap|--blast-app arg"
			assert args.blast_database is not None, "Missed the -bdb|--blast-database arg"
			# assert args.blast_query_sequence is not None, "Missed the -bqs|--blast-query-sequence arg"

			started=datetime.now()
			print("Starting at: %s" % started.strftime("%Y-%m-%d %H:%M:%S"))

			from Bio.Blast import NCBIWWW
			result_handle=None

			# args.blast_query_sequence=''
			# for seq in SeqIO.parse(args.input_file,args.file_input_format):
			# 	args.blast_query_sequence+=seq.id+'\n'

			# if args.blast_query_sequence is not None:
			# if args.verbose:
			# 	print("Searching in BLAST with app %s, in database %s and query %s" % (args.blast_app, args.blast_database, args.blast_query_sequence))
			# 	print("(cmd is %s -db %s)" % (args.blast_app, args.blast_database))
			# result_handle=NCBIWWW.qblast(args.blast_app, args.blast_database, args.blast_query_sequence)
			if args.file_input_format.lower()!="xml":
				try:
					record=SeqIO.read(args.input_file,args.file_input_format)
					result_handle=NCBIWWW.qblast(args.blast_app, args.blast_database, record.seq)
				except ValueError as e: 
					if "more than one record found in handle" in e.args[0].lower():
						records=SeqIO.parse(args.input_file,args.file_input_format)
						query=''
						for rec in records:
							query+=rec.id+'\n'
						print("************query***********")
						print(type(query))
						result_handle=NCBIWWW.qblast(args.blast_app, args.blast_database, query)
						quit()

				with open("blast.xml", 'w') as out_handle:
					# out_handle.write(result_handle.read())
					out_handle.write(result_handle.getvalue())
					# result_handle.close()
			else:
				result_handle = open(args.input_file)

			# else:
			# 	query=''
			# 	for seq in seqs:
			# 		query+="%s\n" % eq

				# result_handle=NCBIWWW.qblast(args.blast_app, args.blast_database, seq)

			from Bio.Blast import NCBIXML
			blast_records = NCBIXML.parse(result_handle)

			for blast_record in blast_records:
				for alignment in blast_record.alignments:
					for hsp in alignment.hsps:
						print("\nALIGNMENT\n")
						print("Sequence: ", alignment.title)
						print("Length: ", alignment.length)
						print("e value: ", hsp.expect)
						print(hsp.query[0:75] + "...")
						print(hsp.match[0:75] + "...")
						print(hsp.sbjct[0:75] + "...")

				# print(blast_record)

			result_handle.close()
			finished=datetime.now()
			print("Finished at: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
			print("Total elapsed time: %s" % str(finished-started))
	else:
		alignments = pairwise2.align.globalxx(seq1, seq2)
		for alignment in alignments: 
			print(pairwise2.format_alignment(*alignment))
		# alignments = pairwise2.align.globalxx(nucleotides[0], nucleotides[1])
		# for alignment in alignments: 
		# 	print(alignment) 

@ray.remote(num_cpus=nproc)
def __ray_align_sequences__(args=None,seqs=None):
	__align_sequences__(args,seqs)

def main(*args):
	args = __parse_args__()
	if args.using_ray:
		ray.init()

	if args.input_file is not None:
		assert args.file_input_format is not None, "Missed the file input format at main(*args)"

		__align_sequences__(args,None)
	else:
		results_search=__retrieve_data__(args)
		seqs=__fetch_seqs__(args,results_search["IdList"])
		args.input_file="tmp.fasta"
		if args.using_ray is None or not args.using_ray:
			# __align_sequences__(args,None)
			__align_sequences__(args,seqs)
		elif args.using_ray:
			# id=__ray_align_sequences__.remote(args,None)
			id=__ray_align_sequences__.remote(args,seqs)
			ray.get(id)

if __name__ == '__main__':
  main(*sys.argv[1:])