# intween.py
#
# Forked from https://github.com/PiPeep/PiTweener
# which was based on caurina Tweener: http://code.google.com/p/tweener/
# which was forked from pyTweener: http://wiki.python-ogre.org/index.php/CodeSnippits_pyTweener
#
# Copyright (c) 2014, Refer accompanying contributors.txt file for authors.
# Refer accompanying LICENSE file for the applicable licensing terms.
#

import time
import math

class tweenStyle(object):
	def __init__(self):
		pass

	def evaluate(self):
		return 0

class DUMMY(tweenStyle):
	def __init__(self, **kwargs):
		super(DUMMY, self).__init__(**kwargs)

	def evaluate(self, t, b, c, d):
		return 0

class MOTION_DESIGN(tweenStyle):
	def __init__(self, **kwargs):
		filenameMd = None
		if "filenameMd"  in kwargs:
			filenameMd = kwargs.pop("filenameMd")

		super(MOTION_DESIGN, self).__init__(**kwargs)

		self.listMd = None
		self.filenameMd = filenameMd
		self.loadMotionDesign()

	def loadMotionDesign(self):
		if None != self.filenameMd :
			fileMd = open(self.filenameMd)
			# IMP : Add checks
			contents = fileMd.readlines()
			fileMd.close()

			if 0 < len(contents):
				self.listMd = []
				for item in contents:
					value = float(item)
					self.listMd.append(value)

			#print self.listMd

	def evaluate(self, t, b, c, d):
		#print "self.filenameMd", self.filenameMd
		return 0 # c * t / d + b

class LINEAR(MOTION_DESIGN):
	def __init__(self, **kwargs):
		super(LINEAR, self).__init__(**kwargs)

	def evaluate(self, t, b, c, d):

		eval_value = 0

		eval_linear_value = t / d

		if None != self.listMd :
			lenSample = len(self.listMd)
			indexSample = eval_linear_value * (lenSample - 1)
			new_indexSample = round(indexSample)
			eval_value = self.listMd[int(new_indexSample)]

		else:
			eval_value = c * t / d + b

		return eval_value



def OUT_EXPO(t, b, c, d):
	if t == d:
		return b + c
	return c * (-2 ** (-10 * t / d) + 1) + b;

def IN_QUAD(t, b, c, d):
	t /= d
	return c * t * t + b

def OUT_QUAD(t, b, c, d):
	t /= d
	return -c * t * (t - 2) + b

def IN_OUT_QUAD(t, b, c, d):
	t /= d * .5
	if t < 1.:
		return c * .5 * t * t + b
	t -= 1.
	return -c * .5 * (t * (t - 2.) - 1.) + b

def OUT_IN_QUAD(t, b, c, d):
	if t < d * .5:
		return self.OUT_QUAD(t * 2, b, c * .5, d)
	return self.IN_QUAD(t * 2 - d, b + c * .5, c * .5, d)

def IN_CUBIC(t, b, c, d):
	t /= d
	return c * t * t * t + b

def OUT_CUBIC(t, b, c, d):
	t = t / d - 1
	return c * (t * t * t + 1) + b

def IN_OUT_CUBIC(t, b, c, d):
	t /= d * .5
	if t < 1:
		 return c * .5 * t * t * t + b
	t -= 2
	return c * .5 * (t * t * t + 2) + b

def OUT_IN_CUBIC(t, b, c, d ):
	if t < d * .5:
		return self.OUT_CUBIC (t * 2., b, c * .5, d)
	return self.IN_CUBIC(t * 2. - d, b + c * .5, c * .5, d)

def IN_QUART(t, b, c, d):
	t /= d
	return c * t * t * t * t + b

def OUT_QUART(t, b, c, d):
	t = t / d - 1
	return -c * (t * t * t * t - 1) + b

def IN_OUT_QUART(t, b, c, d):
	t /= d * .5
	if t < 1:
		return c * .5 * t * t * t * t + b
	t -= 2
	return -c / 2 * (t * t * t * t - 2) + b

def OUT_ELASTIC(t, b, c, d):
	if t == 0:
		return b
	t /= d
	if t == 1:
		return b + c
	p = d * .3 # period
	a = 1. # amplitude
	if a < abs(c):
		a = c
		s = p / 4
	else:
		s = p / (2. * math.pi) * math.asin(c / a)

	return (a * 2. ** (-10. * t) * math.sin((t * d - s) * (2. * math.pi)/ p) + c + b)



class tween(object):
	def __init__(self, sprite, tweentype, duration, delay, cbOnStart, cbOnComplete, cbAfterUpdate, **kwargs):
		self.sprite = sprite
		self.tweentype = tweentype
		self.duration = duration
		self.delay = delay
		self.cbOnStart = cbOnStart
		self.cbOnComplete = cbOnComplete
		self.cbAfterUpdate = cbAfterUpdate

		self.tweenables = kwargs

		self.bComplete = False
		self.bPaused = self.delay > 0
		self.bPauseDelay = 0

		self.delta = 0

		self.t_props = []

		self.setup()

	def remove(self):
		self.bComplete = True

	def pause(self, nSeconds = -1):
		self.bPaused = True
		self.bPauseDelay = nSeconds

	def resume(self):
		if self.bPaused:
			self.bPaused = False

	def setup(self):
		if len(self.tweenables) == 0:
			raise BaseException("No Tweenable properties or functions defined")
			self.bComplete = True
			return

		for prop, final_val in self.tweenables.items():
			start_val = getattr(self.sprite, prop)
			if not hasattr(start_val, "__call__"):
				change = final_val - start_val
				new_prop = [prop, start_val, change]
				self.t_props.append(new_prop)

	def update(self, time_since_last_update):
		if True == self.bPaused:

			if self.delay > 0:
				self.delay = max(0, self.delay - time_since_last_update)

				if self.delay == 0:
					self.bPaused = False
					self.delay = -1

		else:

			self.delta = min(self.delta + time_since_last_update, self.duration)

			if not self.bComplete:
				for prop, start_value, change  in self.t_props:
					newValue = self.tweentype.evaluate(self.delta, start_value, change, self.duration)
					setattr(self.sprite, prop, newValue)

			if self.delta == self.duration:
				self.bComplete = True

			if None != self.cbAfterUpdate:
				self.cbAfterUpdate()

			if True == self.bComplete:
				if None != self.cbOnComplete:
					self.cbOnComplete()

class tweenContext(object):
	def __init__(self, **kwargs):
		self.dictTweens = {}
		self.prev_time = time.time()

	def remove_all_tweens(self):
		for key,value in self.dictTweens.iteritems():
			spriteTweenCollection = value

			for attr,tween in spriteTweenCollection.iteritems():
				tween.remove()

	def get_tweens_affecting_sprite(self, oSprite):
		dictTweensCopy = None
		if self.dictTweens.has_key(oSprite):
			dictTweensCopy = self.dictTweens.copy()
		else :
			dictTweensCopy = {}

		return dictTweenCopy

	def remove_tweening_for(self, oSprite):
		if self.dictTweens.has_key(oSprite):
			spriteTweenCollection = self.dictTweens[oSprite]

			for attr,tween in spriteTweenCollection.iteritems():
				tween.remove()

	def has_tweens(self):
		nReturn = len(self.dictTweens)
		return nReturn

	def has_tweens_for(self, oSprite):
		nReturn = 0
		if self.dictTweens.has_key(oSprite):
			spriteTweenCollection = self.dictTweens[oSprite]
			nReturn = len(spriteTweenCollection)

		return nReturn

	def add_tween(self, oSprite, tweentype, duration, delay, cbOnStart, cbOnComplete, cbAfterUpdate, **kwargs):
		newTween = None

		if not self.dictTweens.has_key(oSprite):
			self.dictTweens[oSprite] = {}

		spriteTweenCollection = self.dictTweens[oSprite]

		for key,value in kwargs.iteritems():
			if not spriteTweenCollection.has_key(key):
				newTween = tween(oSprite, tweentype, duration, delay, cbOnStart, cbOnComplete, cbAfterUpdate, **kwargs)
				spriteTweenCollection[key] = newTween

		return newTween

	def update(self, time_since_last_update=None):

		current_time = time.time()

		if time_since_last_update is None:
			time_since_last_update = current_time - self.prev_time

		# Outer loop
		for key in self.dictTweens.keys():
			spriteTweenCollection = self.dictTweens[key]

			# Inner loop
			for attr in spriteTweenCollection.keys():
				tween = spriteTweenCollection[attr]

				tween.update(time_since_last_update)
				if tween.bComplete:
					del spriteTweenCollection[attr]

			if 0 == len(spriteTweenCollection):
				del self.dictTweens[key]

		self.prev_time = current_time

class tweenSprite(object):
	def __init__(self, **kwargs):
		self.name = "Name_unassigned"
		self.oTweenContext = None

		self.listTweens = []

	#def has_tweens(self):
	#	# IMP : OPTIMIZE
	#	#if None != self.oTweenContext :
	#	#	return self.oTweenContext.has_tweens_for(self)
	#	return len(self.listTweens)

	def add_tween(self, **kwargs):
		if "context" in kwargs:
			self.oTweenContext = kwargs.pop("context")

		tween_type = LINEAR
		if "tween_type" in kwargs:
			tweentype = kwargs.pop("tween_type")

		duration = 1.0
		if "duration" in kwargs:
			duration = kwargs.pop("duration")

		delay = 0.0
		if "delay" in kwargs:
			delay = kwargs.pop("delay")

		cbOnStart = None
		if "cbOnStart"  in kwargs:
			cbOnStart = kwargs.pop("cbOnStart")

		cbOnComplete = None
		if "cbOnComplete"  in kwargs:
			cbOnComplete = kwargs.pop("cbOnComplete")

		cbAfterUpdate = None
		if "cbAfterUpdate"  in kwargs:
			cbAfterUpdate = kwargs.pop("cbAfterUpdate")

		newTween = self.oTweenContext.add_tween(self, tweentype, duration, delay, cbOnStart, cbOnComplete, cbAfterUpdate, **kwargs)
		self.listTweens.append(newTween)

	#def update(self):
	#	# IMP : OPTIMIZE
	#	if None != self.oTweenContext :
	#		return self.oTweenContext.update(self)

class testSprite(tweenSprite):
	def __init__(self, **kwargs):
		super(testSprite, self).__init__(**kwargs)
		self.rot = 0

	def onStart_sample(self):
		print "tween start"

	def onComplete_sample(self):
		print "tween complete"

	def customUpdate(self):
		self.rot = (self.rot + 1) % 360

	def afterUpdate_sample(self):
		#print "rot:",
		print self.rot

if "__main__" == __name__ :

	print "Started ..."
	print

	oTweenType = LINEAR(filenameMd="../app/md/ex1.md")

	oTweenContext = tweenContext()

	oSprite = testSprite()
	oSprite.name = "oSprite"

	tween_sample = oSprite.add_tween(
		context=oTweenContext,
		rot=10,
		tween_type=oTweenType,
		duration=2.0,
		#delay=5,
		#customUpdate=oSprite.customUpdate,
		cbOnStart=oSprite.onStart_sample,
		cbOnComplete=oSprite.onComplete_sample,
		cbAfterUpdate=oSprite.afterUpdate_sample
		)

	#for i in range(0,100):
	while oTweenContext.has_tweens():
		oTweenContext.update()
		#print
		time.sleep(.1)

	print "Done"
