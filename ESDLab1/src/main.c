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

//Function declarations
void readUSARTMessage(void);
void publishUSARTMessage(uint8_t *, uint8_t);
void playSound(uint8_t);

volatile uint8_t received_byte;
volatile uint8_t received_message[] = "a";
volatile uint8_t receive_len = 1;

int main (void)
{
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