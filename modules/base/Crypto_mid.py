import rsa
import sys

class rsa_mid(object):
	def __init__(self):
		try:
			self.read_key()
		except Exception as e:
			res = input('RSA key files not found, create?(y/n)')
			
	def read_key(self):
		with open('public.pem','r') as f:
			self.pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
		with open('private.pem','r') as f:
			self.privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
		
	def enc(self,message):
		enc=rsa.encrypt(message.encode(),self.pubkey)
		return enc

	def dec(self,message):
		dec=rsa.decrypt(message,self.privkey).decode()
		return dec
	
	def new_key(self):
		(self.pubkey,self.privkey)=rsa.newkeys(1024)
		with open('public.pem','w+') as f:
			f.write(self.pubkey.save_pkcs1().decode())
		with open('private.pem','w+') as f:
			f.write(self.privkey.save_pkcs1().decode())
			

rsa_cookie=rsa_mid()
