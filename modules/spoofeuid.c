/* When preloaded, this module overrides the builtin geteuid() function,
 * returning a value of your choice.
 */

int geteuid() {
	return 100;
}

