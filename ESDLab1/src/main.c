/**
 * \file
 *
 * \brief Empty user application template
 *
 */

/**
 * \mainpage User Application template doxygen documentation
 *
 * \par Empty user application template
 *
 * Bare minimum empty user application template
 *
 * \par Content
 *
 * -# Include the ASF header files (through asf.h)
 * -# "Insert system clock initialization code here" comment
 * -# Minimal main function that starts with a call to board_init()
 * -# "Insert application code here" comment
 *
 */

/*
 * Include header files for all drivers that have been imported from
 * Atmel Software Framework (ASF).
 */
/*
 * Support and FAQ: visit <a href="https://www.microchip.com/support/">Microchip Support</a>
 */


#include <asf.h>
#include <conf_usart.h>
#include <stdio.h>
#include <tc.h>
#include <board.h>
#include <compiler.h>
#include <gpio.h>
#include <nvm.h>
#include <sysclk.h>

#define F_CPU sysclk_get_cpu_hz()

#ifdef __GNUC__
#  include <util/delay.h>
#else
static inline void _delay_ms(uint16_t t)
{
	uint16_t i;

	for (i = 0; i < t; ++i) {
		__delay_cycles(F_CPU / 6000);
	}
}
#endif

//Function declarations
void readUSARTMessage(void);
void publishUSARTMessage(uint8_t *, uint8_t);
void playSound(uint8_t);
static void adc_handler(ADC_t *, uint8_t, adc_result_t);
void intToCharArray(uint16_t);

volatile uint8_t received_byte;
volatile uint8_t received_message[] = "a";
volatile uint8_t receive_len = 1;
uint8_t success_str[] = "\n\rSuccess!\n\r";
uint8_t success_len = 12;
static uint16_t tempsense;					//Temperature sensor calibration data.
static volatile uint16_t last_temperature;	//The latest, computed temperature.
volatile uint8_t tempArray[] = "0000";

int main (void)
{
	struct adc_config         adc_conf;
	struct adc_channel_config adcch_conf;
	
	/* Initialize the board.
	 * The board-specific conf_board.h file contains the configuration of
	 * the board initialization.
	 */
	board_init();
	sysclk_init();
	sleepmgr_init();
	irq_initialize_vectors();
	cpu_irq_enable();
	
	// USART options.
	static usart_rs232_options_t USART_SERIAL_OPTIONS = {
		.baudrate = USART_SERIAL_BAUDRATE,
		.charlength = USART_SERIAL_CHAR_LENGTH,
		.paritytype = USART_SERIAL_PARITY,
		.stopbits = USART_SERIAL_STOP_BIT
	};

	// Initialize USART driver in RS232 mode
	usart_init_rs232(USART_SERIAL, &USART_SERIAL_OPTIONS);

	// Initialize ADC configuration structures.
	adc_read_configuration(&ADCA, &adc_conf);
	adcch_read_configuration(&ADCA, ADC_CH0, &adcch_conf);

	/* Configure the ADC module:
	 * - unsigned, 12-bit results
	 * - bandgap (1 V) voltage reference
	 * - 200 kHz maximum clock rate
	 * - manual conversion triggering
	 * - temperature sensor enabled
	 * - callback function
	 */
	adc_set_conversion_parameters(&adc_conf, ADC_SIGN_OFF, ADC_RES_12,
			ADC_REF_BANDGAP);
	adc_set_clock_rate(&adc_conf, 200000UL);
	adc_set_conversion_trigger(&adc_conf, ADC_TRIG_MANUAL, 1, 0);
	adc_enable_internal_input(&adc_conf, ADC_INT_TEMPSENSE);

	adc_write_configuration(&ADCA, &adc_conf);
	adc_set_callback(&ADCA, &adc_handler);

	/* Configure ADC channel 0:
	 * - single-ended measurement from temperature sensor
	 * - interrupt flag set on completed conversion
	 * - interrupts disabled
	 */
	adcch_set_input(&adcch_conf, ADCCH_POS_TEMPSENSE, ADCCH_NEG_NONE,
			1);
	adcch_set_interrupt_mode(&adcch_conf, ADCCH_MODE_COMPLETE);
	adcch_enable_interrupt(&adcch_conf);

	adcch_write_configuration(&ADCA, ADC_CH0, &adcch_conf);
	
	// Get measurement for 85 degrees C (358 kelvin) from calibration data.
	tempsense = adc_get_calibration_data(ADC_CAL_TEMPSENSE);
	// Enable the ADC 
	adc_enable(&ADCA);
	
	//Test ADC
	while (true) {
		//Add Delay
		adc_start_conversion(&ADCA, ADC_CH0);
		_delay_ms(2000);
	}
	
	//Testing out USART Functions
	
	/*uint8_t * a, chartemp;
	uint8_t str[] = "\n\rHello!\n\r";
	uint8_t length = 10;
	bool flag = true;
	
	while(flag){
		readUSARTMessage();
		publishUSARTMessage(received_message,receive_len);
		if(received_message[0] == '1') 
			flag = false;
	}
	
	publishUSARTMessage(str,length);
	
	chartemp = 'a';
	//a = &chartemp;
	for(; chartemp <= 'z'; chartemp++) {
		publishUSARTMessage(&chartemp,1);
	}*/
	
	
}

//Function definitions

/*	
*	Send message on USART
*	str		-	Pointer to char array to be sent
*	length	-	Length of char array to be sent
*/
void publishUSARTMessage(uint8_t *str, uint8_t length) {
	for (int i = 0; i < length; i++) {
		usart_putchar(USART_SERIAL, str[i]);
	}
}

/*
*	Receive message on USART
*	Returns pointer to received message
*/
void readUSARTMessage(void) {
	for(uint8_t i = 0; i<receive_len ; i++) {
		received_byte = usart_getchar(USART_SERIAL);
		//Check which char was received
 		//publishUSARTMessage(&received_byte,1);
		if(received_byte == '$')
			break;
		received_message[i] = received_byte;
	}
	//uint8_t *ret = &received_message;
	//return &received_message[0];
}

/*
*	Function to play sound from speaker
*	index	-	var to identify which sound to play
*/
void playSound(uint8_t index) {
	//Insert code here
}

/**
 * \brief Callback function for ADC interrupts
 *
 * \param adc Pointer to ADC module.
 * \param ch_mask ADC channel mask.
 * \param result Conversion result from ADC channel.
 */
static void adc_handler(ADC_t *adc, uint8_t ch_mask, adc_result_t result) {
	//publishUSARTMessage(success_str,success_len);
	
	uint32_t temperature;

	/* Compute current temperature in kelvin, based on the factory
	 * calibration measurement of the temperature sensor. The calibration
	 * has been done at 85 degrees Celsius, which corresponds to 358 kelvin.
	 */
	temperature = (uint32_t)result * 358;
	temperature /= tempsense;

	// Store temperature in global variable.
	last_temperature = temperature & 0xffff;
	sprintf(tempArray,"%d",last_temperature);
	publishUSARTMessage(tempArray,4);
	// Start next conversion.
	//adc_start_conversion(adc, ch_mask);
}

void intToCharArray(uint16_t num) {
	/*uint8_t n = log10(num) + 1;
	uint8_t i;
	for(i=0; i<n; i++) {
		
	}*/
	sprintf(tempArray,"%d",num);
}