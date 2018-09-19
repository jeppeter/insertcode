#! /usr/bin/env perl

use strict;
use warnings;

if (scalar(@ARGV) >= 2) {
	my ($f) = shift @ARGV;
	my ($t) = shift @ARGV;
	my ($cmd) = "cp -f $f $t";
	system($cmd);
}