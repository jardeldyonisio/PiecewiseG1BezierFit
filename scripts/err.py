import ktangdt
import ctpts
import sod

def err(x0, Q, k):
	'''
	This function computes the distance error for the curve.
	'''
	# Call to separates x0 into its subcomponents.
	P, ang, dt = ktangdt(x0)
	# Call to compute control points.
	C = ctpts(P, ang, dt)

	# Call to compute distance error for the curve.
	error = sod(C, Q, k)

	return error