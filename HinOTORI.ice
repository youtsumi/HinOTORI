module HinOTORI {

	exception Error {
		string reason;
	};

	interface Camera { 
		["amd"] void Take( 
			double expt, 
			string filename, 
			bool shutter,
			string header )
			throws Error;
		double GetTemperature(  );
		void SetTemperature( double setp );
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
		double GetAz(  );
		double GetEl(  );
		void SetRa( double radeg );
		void SetDec( double decdeg );
		void Goto( );
	};

	interface Dome {
		void slitOpen( );
		void slitClose( );
		int CurrentDirection();
		int TargetDirection();
		bool Alarm1();
		bool Alarm2();
		bool Alarm3();
		bool isSlitOpened();
		bool isSlitClosed();
		bool isDomeOrigin();
	};
};
