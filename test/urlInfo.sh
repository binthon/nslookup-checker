#!/bin/bash

domains_file="domains.txt"
results_file="tracert_results.txt"

if [ ! -f "$domains_file" ]; then
    echo "Nie znaleziono pliku z domenami."
    exit 1
fi


while IFS= read -r domain; do
    echo "Tracert dla $domain na dzień $(date '+%Y-%m-%d %H:%M:%S')" >> "$results_file"
    
    failed_attempts=0


    traceroute "$domain" | while IFS= read -r line; do
        echo "$line" >> "$results_file"
        
        if [[ "$line" == *"* * *" ]]; then
            ((failed_attempts++))
        else
            failed_attempts=0
        fi
        
        if [ "$failed_attempts" -eq 3 ]; then
            break
        fi
    done

done < "$domains_file"

echo "Zakończono przetwarzanie domen."
exit 0
