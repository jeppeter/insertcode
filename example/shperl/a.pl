#! /usr/bin/env perl

use strict;
use Cwd "abs_path";
use File::Basename;
use Getopt::Long;
use File::Spec;

sub Usage($$)
{
	my ($ec,$fmt)=@_;
	my ($fp)=\*STDERR;

	if ($ec == 0) {
		$fp =\*STDOUT;
	}

	if (length($fmt) > 0) {
		print $fp "$fmt\n";
	}

	print $fp "$0 [OPTIONS]  [dirs]...\n";
	print $fp "[OPTIONS]\n";
	print $fp "\t-h|--help               to give this help information\n";
	print $fp "\t-v|--verbose            to make verbose mode\n";
	print $fp "\n";
	print $fp "\t[dirs]                  if will give basename of it\n";

	exit($ec);
}

my $logo="basename";


use Cwd "abs_path";
use File::Basename;
use File::Spec;


my ($verbose)=0;

sub Debug($)
{
	my ($fmt)=@_;
	my ($fmtstr)="$logo ";
	if ($verbose > 0) {
		if ($verbose >= 3) {
			my ($p,$f,$l) = caller;
			$fmtstr .= "[$f:$l] ";
		}
		$fmtstr .= $fmt;
		print STDERR "$fmtstr\n";
	}
}

sub Error($)
{
	my ($fmt)=@_;
	my ($fmtstr)="$logo ";
	if ($verbose >= 3) {
		my ($p,$f,$l) = caller;
		$fmtstr .= "[$f:$l] ";
	}
	$fmtstr .= $fmt;
	print STDERR "$fmtstr\n";
}

sub FinalOutput($)
{
	my ($output) = @_;
	if ($output && -t STDOUT) {
		print "\n";
	}
}

sub GetFullPath($)
{
	my ($c) =@_;
	if ( -e $c && !( -l $c) ) {
		return abs_path($c);
	}
	return File::Spec->rel2abs($c);
}

sub TrimRoot($)
{
	my ($c) = @_;
	my $curch;
	while (length($c) > 0 ) {
		$curch = substr($c,0,1);
		if ($curch eq "/" ||
			$curch eq "\\") {
			$c =~ s/.//;
		} else {
			last;
		}
	}
	return $c;
}

sub format_out($$$@)
{
	my ($simple,$hashref,$notice,@vals)=@_;
	my ($outstr)="";
	my (@arr);
	foreach (@vals) {
		my ($curval) = $_;
		if (defined($hashref->{$curval})) {
			if ($simple) {
				if (ref ($hashref->{$curval}) eq "ARRAY") {
					@arr = @{$hashref->{$curval}};
					foreach (@arr) {
						$outstr .= "$_\n";	
					}
				} else{
					$outstr .= $hashref->{$curval}."\n";
				}
			} else {
				if (ref ($hashref->{$curval}) eq "ARRAY") {
					@arr = @{$hashref->{$curval}};
					foreach (@arr) {
						$outstr .= "$_ $curval $notice\n";
					}
				} else {
					$outstr .= $hashref->{$curval}." $curval $notice\n";
				}
			}
		}
	}
	return $outstr;
}

sub trimspace($)
{
	my ($retl)=@_;
	$retl =~ s/^\s+//;
	$retl =~ s/\s+$//;
	return $retl;
}


my %opts;
Getopt::Long::Configure("no_ignorecase","bundling");
Getopt::Long::GetOptions(\%opts,"help|h",
	"verbose|v" => sub {
		if (!defined($opts{"verbose"})) {
			$opts{"verbose"} = 0;
		}
		${opts{"verbose"}} ++;
	});

if (defined($opts{"help"})) {
	Usage(0,"");
}

if (defined($opts{"verbose"})) {
	$verbose = $opts{"verbose"};
}

foreach(@ARGV) {
	my ($c) = $_;
	$c = GetFullPath($c);
	Debug("[$c]");
	print basename($c)."\n";
}
