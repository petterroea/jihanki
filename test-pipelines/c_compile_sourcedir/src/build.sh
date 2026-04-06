#!/bin/sh

ls -laht /

cc -D PERSON_NAME=\"$PERSON_NAME\" -static main.c -o /output/main
