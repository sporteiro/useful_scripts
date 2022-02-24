<?php

class WorkingDays {

	public $workingdays_array;

	public function main($start)  {

        //set the period we want to obtain working days from
        //$start = "2022-01-01";
        $begin = new DateTime($start);
        $end = new DateTime($start);
        $end = $end->modify( '+365 days' );
        
        //create an array for notworkingdays, it can be populate with bank holidays or any other non working day
        $notworkingdays_array = array();
        //create an array for working days;
        $workingdays_array = array();

        //interval for all days of the first period
        $interval = new DateInterval('P1D');
        $daterange = new DatePeriod($begin, $interval ,$end);


        //populate notworkingdays_array with weekends
        foreach($daterange as $date) {
            if ($this->isWeekend($date)==1)	{
                array_push($notworkingdays_array,$date->format("Y-m-d"));
            }
        } 
        //populate working_days array
        foreach($daterange as $date) {
            if (!in_array($date->format("Y-m-d"), $notworkingdays_array)) {
                array_push($workingdays_array,$date->format("Y-m-d"));
            }
        }  
        return $workingdays_array;
    }
    //check if a given date is a weekend
    public function isWeekend($date) {
        return $date->format('N') >= 6;
    }
}      
$obj = new WorkingDays();
print_r($obj->main("2022-01-01"));
?>
