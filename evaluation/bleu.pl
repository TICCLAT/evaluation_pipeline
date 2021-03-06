#!/usr/bin/perl -w
# bleu: compare two texts with bleu score
# usage: bleu [-s] translatedFile referenceFile
# notes:a
# * beware of file order in arguments: different order => different results!
# * option -s: perform cleanup of input lines: _=>" "; +=>""; DELETED=>""
# * compared with: multi-bleu.perl
# https://github.com/moses-smt/mosesdecoder/blob/master/scripts/generic/multi-bleu.perl
# 20150903 erikt(at)xs4all.nl
# 20170213 current version

use strict;
use Getopt::Std;

my $command = $0;
my $MAXNGRAM = 4;
my %options = ();
getopts("s",\%options);

my $translated = shift(@ARGV);
my $reference = shift(@ARGV);
if (not defined $reference) { 
   die "usage: $command translatedFile referenceFile\n"; 
}
if ($translated eq "-") { open(TRANSLATED,"<&STDIN"); }
elsif (not open(TRANSLATED,$translated)) {
   die "$command: cannot read file $translated\n";
}
if ($reference eq "-") { open(REFERENCE,"<&STDIN"); }
elsif (not open(REFERENCE,$reference)) {
   die "$command: cannot read file $reference\n";
}
my $s = 0; # number of lines/sentences (should be the same in both files)
my $bleuScore = 0; # bleu score
my $tLength = 0;   # number of tokens in the translated text
my $rLength = 0;   # number of tokens in the reference text
my @pScores = ();  # number of indentical ngrams on both lines (case sensitive)
my @pTotals = ();  # number of ngrams in the translated text
while (<TRANSLATED>) {
   my $tLine = $_; # translated line
   chomp($tLine);
   if (defined $options{"s"}) { $tLine = &cleanup($tLine); }
   $tLength += split(/\s+/,$tLine);
   my $rLine = <REFERENCE>; # reference line
   if (not defined $rLine) { 
      die "$command: too few lines in reference file!\n";
   }
   chomp($rLine);
   if (defined $options{"s"}) { $rLine = &cleanup($rLine); }
   $rLength += split(/\s+/,$rLine);
   for (my $n=1;$n<=$MAXNGRAM;$n++) {
      my %tNgrams = &getNgrams($n,$tLine);
      my %rNgrams = &getNgrams($n,$rLine);
      my ($score,$total) = &compareNgrams(\%tNgrams,\%rNgrams);
      $pScores[$n] = defined $pScores[$n] ? $pScores[$n]+$score : $score;
      $pTotals[$n] = defined $pTotals[$n] ? $pTotals[$n]+$total : $total;
   }
   $s++;
}
if (<REFERENCE>) { die "$command: too many lines in reference file!\n"; }
close(REFERENCE);
close(TRANSLATED);
# compute n-gram precisions: number of matches divided by total
for (my $n=1;$n<=$MAXNGRAM;$n++) { 
   $pScores[$n] /= $pTotals[$n] > 0 ? $pTotals[$n] : 1;
   # bleu score is (exponent of) geometric average of ngram precision scores
   if ($pScores[$n] > 0) { $bleuScore += log($pScores[$n])/$MAXNGRAM; }
}
$bleuScore = exp($bleuScore);
# multiply with brevity penalty if the translated text is shorter
my $BP = ($tLength < $rLength) ? exp(1-$rLength/$tLength) : 1.0; 
$bleuScore *= $BP;
printf "processed %d sentences; bleu score = %0.5f\n",$s,$bleuScore;

exit(0);

sub getNgrams() {
   my $n = shift(@_);
   my $line = shift(@_);
   if (not defined $line) { 
      die "$command: function getNgrams requires an argument\n"; 
   }
   my @t = split(/\s+/,$line);
   my %ngrams = ();
   for (my $i=0;$i<=$#t-$n+1;$i++) {
      my $ngram = $t[$i];
      for (my $j=1;$j<$n;$j++) { $ngram .= " ".$t[$i+$j]; }
      $ngrams{$ngram} = defined $ngrams{$ngram} ? $ngrams{$ngram}+1 : 1;
   }
   return(%ngrams);
}

sub compareNgrams() {
   my ($tNgramsRef,$rNgramsRef) = @_;
   if (not defined $rNgramsRef) { 
      die "$command: function compareNgrams requires two arguments\n"; 
   }
   my %tNgrams = %{$tNgramsRef};
   my %rNgrams = %{$rNgramsRef};
   my $tLength = 0;
   my $score = 0;
   foreach my $key (keys %tNgrams) { $tLength += $tNgrams{$key}; }
   foreach my $key (keys %tNgrams) {
      if (defined $rNgrams{$key}) {
         if ($tNgrams{$key} < $rNgrams{$key}) { $score += $tNgrams{$key}; } 
         else { $score += $rNgrams{$key}; }
      }
   }
   return($score,$tLength);
}

# cleanup function for CLIN2017 shared task data lines
sub cleanup() {
   my $line = shift(@_);
   $line =~ s/_/ /g; # split words like datse=>dat_ze
   $line =~ s/\+//g; # combined words like in dien=>in+dien
   $line =~ s/^\s+//;
   $line =~ s/\s+$//;
   my @tokens = split(/\s+/,$line);
   for (my $i=0;$i<=$#tokens;$i++) {
      if ($tokens[$i] eq "DELETED") { 
         # deleted tokens
         splice(@tokens,$i,1);
         $i--;
      }
   }
   $line = join(" ",@tokens);
   return($line);
}
