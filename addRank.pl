#!/usr/bin/perl

use strict;

my $input = shift;

open(FILE, $input) || die "Cant open file. Reason: $!";
my @content=<FILE>;
close(FILE);

my $line;

my $newRank = 1;
foreach $line (@content)
{
   chomp $line;
   printf ("%s %11d\n", $line, $newRank++);
}
