import requests
from lxml import html
import matplotlib.pyplot as plt
from string import ascii_uppercase
from collections import Counter

def main():
	base_url = 'https://www.pro-football-reference.com/players/'
	d = {}
	total_career_lengths = []
	for c in ascii_uppercase:
		url = base_url + c + '/'
		req = requests.get(url)
		tree = html.fromstring(req.content)
		players = tree.xpath('//*[@id="div_players"]/p/a/text()')
		info = tree.xpath('//*[@id="div_players"]/p/text()')
		data = list(zip(players, info))
		
		split = [ i.strip().split(')') for i in info]
		years = [(s[1].split('-')) for s in split if len(s) > 1]
		years = map(lambda x: (float(x[0]), float(x[1])), years)
		career_lengths = [y[1]-y[0] for y in years]
		d[c] = career_lengths
		total_career_lengths = total_career_lengths + career_lengths
		if c == 'B':
			print(data)
		print(f'{c} - Done')
	counts = list(Counter(total_career_lengths).items())
	counts_dict = {c[0]:c[1] for c in counts}
	max_years = max(counts, key=lambda x: x[0])[0]
	x_vals = range(0, int(max_years))
	y_vals = [0 if not x in counts_dict.keys() else counts_dict[x] for x in x_vals]
	plt.style.use('ggplot')
	plt.barh(x_vals, y_vals, color='red')
	plt.xlabel('Years in NFL')
	plt.ylabel('Number of Players')
	plt.title('Number of Years NFL Players are a Part of the NFL')
	for i, v in enumerate(y_vals):
		plt.text(v, i, str(v), color='red', fontweight='bold')

	mean = sum(total_career_lengths) / len(total_career_lengths)
	total_career_lengths.sort()
	median = total_career_lengths[int(len(total_career_lengths) / 2)]
	mode, occurences = max(counts, key=lambda x: x[1])

	print(f'Mean: {mean}, median: {median}, mode: {mode} years by {occurences} players')
	plt.text(3000,15,f'Mean: {mean}\nMedian: {int(median)}\nMode: {int(mode)} years by {occurences} players', fontweight='bold')

	plt.show()

if __name__ == '__main__':
	main()