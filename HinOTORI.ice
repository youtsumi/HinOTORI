module HinOTORI {
	["python:seq:tuple"] sequence<string> FitsItem; 
	["python:seq:list"] sequence<FitsItem> FitsHeader; 

	exception Error {
		string reason;
	};

	interface Camera { 
		["amd"] void Take( 
			double expt, 
			string filename, 
			bool shutter,
			FitsHeader header )
			throws Error;
		double GetTemperature(  );
		void SetTemperature(  );
		void TurnOnCooler(  );
	};

	interface Telescope { 
		double GetFocusZ(  );
		void SetFocusZ( double z );
		void OpenMirror(  );
		void CloseMirror(  );
	};

	interface Mount { 
		double GetRa(  );
		double GetDec(  );
		void SetRa( double radeg );
		void SetDec( double decdeg );
		void Goto( );
	};
};
