from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, request
import sqlite3
from api import APICall
import json
import random
import string

app = Flask(__name__)

bad_word_list = ["4r5e", "5h1t", "5hit", "a55", "anal", "anus", "ar5e", "arrse", "arse", "ass", "ass-fucker", "asses", "assfucker", "assfukka", "asshole", "assholes", "asswhole", "a_s_s", "b!tch", "b00bs", "b17ch", "b1tch", "ballbag", "balls", "ballsack", "bastard", "beastial", "beastiality", "bellend", "bestial", "bestiality", "bi+ch", "biatch", "bitch", "bitcher", "bitchers", "bitches", "bitchin", "bitching", "bloody", "blow job", "blowjob", "blowjobs", "boiolas", "bollock", "bollok", "boner", "boob", "boobs", "booobs", "boooobs", "booooobs", "booooooobs", "breasts", "buceta", "bugger", "bum", "bunny fucker", "butt", "butthole", "buttmuch", "buttplug", "c0ck", "c0cksucker", "carpet muncher", "cawk", "chink", "cipa", "cl1t", "clit", "clitoris", "clits", "cnut", "cock", "cock-sucker", "cockface", "cockhead", "cockmunch", "cockmuncher", "cocks", "cocksuck", "cocksucked", "cocksucker", "cocksucking", "cocksucks", "cocksuka", "cocksukka", "cok", "cokmuncher", "coksucka", "coon", "cox", "crap", "cum", "cummer", "cumming", "cums", "cumshot", "cunilingus", "cunillingus", "cunnilingus", "cunt", "cuntlick", "cuntlicker", "cuntlicking", "cunts", "cyalis", "cyberfuc", "cyberfuck", "cyberfucked", "cyberfucker", "cyberfuckers", "cyberfucking", "d1ck", "damn", "dick", "dickhead", "dildo", "dildos", "dink", "dinks", "dirsa", "dlck", "dog-fucker", "doggin", "dogging", "donkeyribber", "doosh", "duche", "dyke", "ejaculate", "ejaculated", "ejaculates", "ejaculating", "ejaculatings", "ejaculation", "ejakulate", "f u c k", "f u c k e r", "f4nny", "fag", "fagging", "faggitt", "faggot", "faggs", "fagot", "fagots", "fags", "fanny", "fannyflaps", "fannyfucker", "fanyy", "fatass", "fcuk", "fcuker", "fcuking", "feck", "fecker", "felching", "fellate", "fellatio", "fingerfuck", "fingerfucked", "fingerfucker", "fingerfuckers", "fingerfucking", "fingerfucks", "fistfuck", "fistfucked", "fistfucker", "fistfuckers", "fistfucking", "fistfuckings", "fistfucks", "flange", "fook", "fooker", "fuck", "fucka", "fucked", "fucker", "fuckers", "fuckhead", "fuckheads", "fuckin", "fucking", "fuckings", "fuckingshitmotherfucker", "fuckme", "fucks", "fuckwhit", "fuckwit", "fudge packer", "fudgepacker", "fuk", "fuker", "fukker", "fukkin", "fuks", "fukwhit", "fukwit", "fux", "fux0r", "f_u_c_k", "gangbang", "gangbanged", "gangbangs", "gaylord", "gaysex", "goatse", "God", "god-dam", "god-damned", "goddamn", "goddamned", "hardcoresex", "hell", "heshe", "hoar", "hoare", "hoer", "homo", "hore", "horniest", "horny", "hotsex", "jack-off", "jackoff", "jap", "jerk-off", "jism", "jiz", "jizm", "jizz", "kawk", "knob", "knobead", "knobed", "knobend", "knobhead", "knobjocky", "knobjokey", "kock", "kondum", "kondums", "kum", "kummer", "kumming", "kums", "kunilingus", "l3i+ch", "l3itch", "labia", "lmfao", "lust", "lusting", "m0f0", "m0fo", "m45terbate", "ma5terb8", "ma5terbate", "masochist", "master-bate", "masterb8", "masterbat*", "masterbat3", "masterbate", "masterbation", "masterbations", "masturbate", "mo-fo", "mof0", "mofo", "mothafuck", "mothafucka", "mothafuckas", "mothafuckaz", "mothafucked", "mothafucker", "mothafuckers", "mothafuckin", "mothafucking", "mothafuckings", "mothafucks", "mother fucker", "motherfuck", "motherfucked", "motherfucker", "motherfuckers", "motherfuckin", "motherfucking", "motherfuckings", "motherfuckka", "motherfucks", "muff", "mutha", "muthafecker", "muthafuckker", "muther", "mutherfucker", "n1gga", "n1gger", "nazi", "nigg3r", "nigg4h", "nigga", "niggah", "niggas", "niggaz", "nigger", "niggers", "nob", "nob jokey", "nobhead", "nobjocky", "nobjokey", "numbnuts", "nutsack", "orgasim", "orgasims", "orgasm", "orgasms", "p0rn", "pawn", "pecker", "penis", "penisfucker", "phonesex", "phuck", "phuk", "phuked", "phuking", "phukked", "phukking", "phuks", "phuq", "pigfucker", "pimpis", "piss", "pissed", "pisser", "pissers", "pisses", "pissflaps", "pissin", "pissing", "pissoff", "poop", "porn", "porno", "pornography", "pornos", "prick", "pricks", "pron", "pube", "pusse", "pussi", "pussies", "pussy", "pussys", "rectum", "retard", "rimjaw", "rimming", "s hit", "s.o.b.", "sadist", "schlong", "screwing", "scroat", "scrote", "scrotum", "semen", "sex", "sh!+", "sh!t", "sh1t", "shag", "shagger", "shaggin", "shagging", "shemale", "shi+", "shit", "shitdick", "shite", "shited", "shitey", "shitfuck", "shitfull", "shithead", "shiting", "shitings", "shits", "shitted", "shitter", "shitters", "shitting", "shittings", "shitty", "skank", "slut", "sluts", "smegma", "smut", "snatch", "son-of-a-bitch", "spac", "spunk", "s_h_i_t", "t1tt1e5", "t1tties", "teets", "teez", "testical", "testicle", "tit", "titfuck", "tits", "titt", "tittie5", "tittiefucker", "titties", "tittyfuck", "tittywank", "titwank", "tosser", "turd", "tw4t", "twat", "twathead", "twatty", "twunt", "twunter", "v14gra", "v1gra", "vagina", "viagra", "vulva", "w00se", "wang", "wank", "wanker", "wanky", "whoar", "whore", "willies", "willy", "xrated", "xxx", "stupid"]
page_token = 'EAANY1zUezt0BAH5qJumEd3ZCBbwXzlVvzHSHPwuc59Gf1zbZAt8U5TZBZCMCW8Jip6fmIaujqS4kLPAXjucPLtT7V7lHtzJLxScc2mEG6CzJmXXC8FkcXT4mkslyQ0vE6WcdNG8TYZCNXK3QuZCAwOALJBG7sS8mC4ZB43frHxSdXPlVPkUVU3T'
page_id = '1214426478643008'

fb = APICall(page_token)

def generateRandom():
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))


def bad_message_warning(user_id):
	# message is bad send warning to sender
	send_to_recipient('Ema: Message Not Sent (contains offensive language)', user_id)


def sentiment_warning(user_id):
	# message has low sentiment score send message to sender
	send_to_recipient('Ema: Message Not Sent (contains hurtful language)', user_id)


def send_to_recipient(message, user_id):
	# get profile from user_id and send message
	link = 'https://graph.facebook.com/v2.8/'+page_id+'/messages'
	data = { 
		"recipient": { 
			"id": user_id 
		},
		"message": { 
			"text": message 
		}
	}
	print fb.makeRequestPost(link, data)


def checkSentiment(message):
	analyzer = SentimentIntensityAnalyzer()
	vs = analyzer.polarity_scores(message)
	if vs['compound'] < 0:
		return True
	return False


def matchInterests(interests):
	conn = sqlite3.connect('ema.db')
	c = conn.cursor()
	for interest in interests.split(' '):
		c.execute('SELECT * FROM conversations WHERE topic="'+interest+'" AND isEnded="false"')
		conversation = c.fetchone()
		if conversation != None:
			conn.commit()
			c.close()
			return conversation
			break
	return None


def getProfile(user_id):
	link = 'https://graph.facebook.com/v2.8/'+user_id
	response = fb.makeRequest(link)
	return json.loads(response)


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
	if request.method == 'POST':
		response = request.get_json()

		if response['object'] == 'page':

			try:
				sender = response['entry'][0]['messaging'][0]['sender']['id']
				message = response['entry'][0]['messaging'][0]['message']['text']
			except:
				return '500'

			if sender == page_id:
				return '500'

			conn = sqlite3.connect('ema.db')
			c = conn.cursor()
			c.execute('SELECT * FROM conversations WHERE user1="'+sender+'" OR user2="'+sender+'" AND isEnded="false"')
			conversation = c.fetchone()

			if conversation != None:
				if (str(conversation[1]) != 'None') & (str(conversation[2]) != 'None'):
					# user is in a conversation with another user
					print 'Conversation Started'
					recipient = conversation[0]
					if sender == recipient:
						recipient = conversation[1]

					if message.lower() != 'stop':
						isBadWord = False
						for msg in message.split(' '):
							for word in bad_word_list:
								if msg.lower() == word.lower():
									isBadWord = True
									break
						if isBadWord:
							bad_message_warning(sender)
						elif checkSentiment(message):
							sentiment_warning(sender)
						else:
							send_to_recipient(message, recipient)
							print 'sent'
					else:
						print 'Conversation Stopped'
						c.execute('UPDATE conversations SET isEnded=\'%s\' WHERE convo_id=\'%s\'' % ("true", conversation[4]))
						conn.commit()
						c.close()
						send_to_recipient('Ema: Conversation Ended', sender)
						send_to_recipient('Ema: Conversation Ended', recipient)
				else:
					# user started conversation but not paired yet
					print conversation
					if str(conversation[3]) != 'None':
						match = matchInterests(message)
						print str(match)
						if match == None:
							print 'New Topic'
							c.execute('UPDATE conversations SET topic=\'%s\' WHERE user1=\'%s\' AND isEnded=\'%s\'' % (message, sender, 'false'))
							conn.commit()
							c.close()
							send_to_recipient('Saved! I will message you when I find a friend with similar interests.', sender)
						else:
							print 'New User'
							if conversation[0] != match[0]:
								c.execute('UPDATE conversations SET user2=\'%s\', topic=\'%s\' WHERE convo_id=\'%s\' AND isEnded=\'%s\'' % (match[0], match[2], conversation[4], 'false'))
								c.execute('DELETE FROM conversations WHERE user1=\'%s\' AND isEnded=\'%s\'' % (match[0], 'false'))
								conn.commit()
								c.close()
								send_to_recipient('Found a friend with similar interests. Say hello to '+getProfile(match[0])['first_name'], sender)
								send_to_recipient('Found a friend with similar interests. Say hello to '+getProfile(sender)['first_name'], match[0])
		
			else:
				print 'New Conversation'
				# user has not started conversation yet
				c.execute('INSERT INTO conversations (user1, isEnded, convo_id) VALUES (\'%s\', \'%s\', \'%s\')' % (sender, 'false', generateRandom()))
				conn.commit()
				c.close()
				send_to_recipient('Hello! What do you want to talk about? What are your interests?', sender)
	return '200'


if __name__ == '__main__':
	app.run(port=80, debug=True)
