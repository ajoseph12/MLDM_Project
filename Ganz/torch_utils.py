

def images_to_vectors(images):

	return images.view(images.size(0), 784)


def vectors_to_images(vectors):

	return vectors.view(vectors.size(0), 1, 28, 28)


def noise(size):

	n = Variable(torch.randn(size, 100))
	if torch.cuda.is_available(): return n.cuda()
	return n

